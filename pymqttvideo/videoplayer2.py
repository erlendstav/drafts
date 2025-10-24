"""MQTT-triggered video player for Raspberry Pi and macOS.

The script subscribes to MQTT topics on the form ``<location>/<action>/<video>``.
The default ``location`` is ``garage`` but can be overridden via CLI. ``action``
is either ``play`` or ``stop`` and ``video`` refers to a file inside the
configured video directory (defaults to ``~/Videos``).

Dependencies:
	- paho-mqtt
	- python-vlc (with VLC installed on the host system)
"""

from __future__ import annotations

import argparse
import logging
import platform
import queue
import signal
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing_extensions import Literal

import paho.mqtt.client as mqtt

try:
	import vlc  # type: ignore
except ImportError as exc:  # pragma: no cover - fail fast if VLC bindings missing
	raise SystemExit(
		"The python-vlc package is required. Install it with 'pip install python-vlc'."
	) from exc


# Quick sanity delay that also lets VLC settle before reuse in rapid sequences.
VLC_RESET_DELAY = 0.2


@dataclass
class PlaybackCommand:
	action: str
	video_name: Optional[str] = None


class VideoLibrary:
	"""Resolve requested video names to actual files."""

	def __init__(self, video_dir: Path) -> None:
		self.video_dir = video_dir
		self._index_lock = threading.Lock()
		self._by_stem: dict[str, Path] = {}
		self._scan_video_dir()

	def _scan_video_dir(self) -> None:
		with self._index_lock:
			self._by_stem.clear()
			if not self.video_dir.exists():
				logging.warning("Video directory %s does not exist", self.video_dir)
				return
			for candidate in self.video_dir.iterdir():
				if candidate.is_file():
					self._by_stem[candidate.stem.lower()] = candidate

	def resolve(self, name: str) -> Optional[Path]:
		"""Return a path for the given name if available."""

		if not name:
			return None

		requested = name.strip()
		if not requested:
			return None

		candidate = Path(requested)
		if candidate.is_absolute() and candidate.exists():
			return candidate

		path = self.video_dir / requested
		if path.exists():
			return path

		# Fall back to stem lookup to allow topics without file extension.
		with self._index_lock:
			match = self._by_stem.get(requested.lower())
			if match and match.exists():
				return match

		# Directory might have changed since start; rescan once.
		self._scan_video_dir()
		with self._index_lock:
			match = self._by_stem.get(requested.lower())
			if match and match.exists():
				return match

		return None


class PlaybackController:
	"""Manage VLC playback in a thread-safe way."""

	def __init__(self, video_dir: Path) -> None:
		self.video_dir = video_dir
		self.library = VideoLibrary(video_dir)
		vlc_args = ["--no-video-title-show", "--fullscreen"] #, "-I macosx"]
		#if platform.system() == "Darwin":
		#	vlc_args.extend(["--vout=macosx", "--aout=coreaudio", "--intf", "dummy"])
		self._vlc_instance = vlc.Instance(*vlc_args)
		self._player = self._vlc_instance.media_player_new()
		self._player.audio_set_mute(False)
		self._lock = threading.Lock()

	def play(self, video_name: str) -> None:
		video_path = self.library.resolve(video_name)
		if not video_path:
			logging.error("Video '%s' not found in %s", video_name, self.video_dir)
			return

		with self._lock:
			if self._player is None:
				logging.error("Playback controller has been closed; ignoring play request")
				return
			logging.info("Starting playback of %s", video_path)
			self._player.stop()
			time.sleep(VLC_RESET_DELAY)
			media = self._vlc_instance.media_new_path(str(video_path))
			self._player.set_media(media)
			if self._player.play() == -1:
				logging.error("Failed to start playback of %s", video_path)
			else:
				# VLC sometimes toggles fullscreen off when reusing a player.
				self._player.set_fullscreen(True)

	def stop(self) -> None:
		with self._lock:
			if self._player is None:
				return
			logging.info("Stopping playback")
			self._player.stop()
			time.sleep(VLC_RESET_DELAY)
			self._player.set_fullscreen(True)

	def close(self) -> None:
		with self._lock:
			if self._player is None:
				return
			self._player.stop()
			self._player.release()
			self._player = None
		if self._vlc_instance is not None:
			self._vlc_instance.release()
			self._vlc_instance = None


class MQTTVideoPlayer:
	"""Wraps MQTT subscription handling for video playback."""

	def __init__(
		self,
		mqtt_host: str,
		mqtt_port: int,
		topic_prefix: str,
		playback: PlaybackController,
		username: Optional[str] = None,
		password: Optional[str] = None,
	) -> None:
		self._mqtt_host = mqtt_host
		self._mqtt_port = mqtt_port
		self._topic_prefix = topic_prefix
		self._playback = playback
		self._queue: "queue.Queue[PlaybackCommand]" = queue.Queue()
		self._stop_event = threading.Event()

		client_id = f"video-player-{topic_prefix}-{int(time.time())}"
		self._client = mqtt.Client(client_id=client_id, clean_session=True)
		if username:
			self._client.username_pw_set(username, password)

		self._client.on_connect = self._handle_connect
		self._client.on_message = self._handle_message
		self._client.on_disconnect = self._handle_disconnect

	# MQTT callbacks -----------------------------------------------------

	def _handle_connect(self, client: mqtt.Client, _userdata, flags, rc) -> None:
		if rc != 0:
			logging.error("MQTT connection failed with code %s", rc)
			return
		topic = f"{self._topic_prefix}/+/+"
		client.subscribe(topic)
		logging.info("Subscribed to %s", topic)

	def _handle_message(self, _client: mqtt.Client, _userdata, message: mqtt.MQTTMessage) -> None:
		parts = message.topic.split("/")
		if len(parts) < 3:
			logging.debug("Ignoring topic without video segment: %s", message.topic)
			return

		location, action, video_name = parts[0], parts[1], parts[2]
		if location != self._topic_prefix:
			logging.debug("Ignoring topic for other location: %s", message.topic)
			return

		action = action.lower()
		if action not in {"play", "stop"}:
			logging.debug("Ignoring unknown action '%s'", action)
			return

		cmd = PlaybackCommand(action=action, video_name=video_name)
		self._queue.put(cmd)

	def _handle_disconnect(self, _client: mqtt.Client, _userdata, rc) -> None:
		if rc != 0:
			logging.warning("Unexpected MQTT disconnect (rc=%s). Reconnecting...", rc)

	# Public API ---------------------------------------------------------

	def run(self) -> None:
		logging.info("Connecting to MQTT broker %s:%s", self._mqtt_host, self._mqtt_port)
		self._client.connect(self._mqtt_host, self._mqtt_port, keepalive=60)
		self._client.loop_start()

		try:
			while not self._stop_event.is_set():
				try:
					cmd = self._queue.get(timeout=0.2)
				except queue.Empty:
					continue

				if cmd.action == "play" and cmd.video_name:
					self._playback.play(cmd.video_name)
				elif cmd.action == "stop":
					self._playback.stop()
		except KeyboardInterrupt:
			logging.info("Interrupted by user")
		finally:
			self.shutdown()

	def shutdown(self) -> None:
		if not self._stop_event.is_set():
			self._stop_event.set()
		self._client.loop_stop()
		self._client.disconnect()
		self._playback.stop()


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Play videos triggered by MQTT topics.")
	parser.add_argument("--mqtt-host", default="192.168.1.50", help="MQTT broker hostname")
	parser.add_argument("--mqtt-port", type=int, default=1883, help="MQTT broker port")
	parser.add_argument("--mqtt-username", help="MQTT username", default=None)
	parser.add_argument("--mqtt-password", help="MQTT password", default=None)
	parser.add_argument("--location", default="garage", help="MQTT topic prefix/location")
	parser.add_argument(
		"--video-dir",
		default=str(Path.home() / "Videos"),
		help="Directory where video files are stored",
	)
	parser.add_argument("--log-level", default="INFO", help="Logging level")
	return parser


def main() -> None:
	parser = build_parser()
	args = parser.parse_args()
	logging.warning("Host " + str(args.mqtt_host))
	logging.warning("Port " + str(args.mqtt_port))

	try:
		logging.basicConfig(
			level=getattr(logging, args.log_level.upper(), logging.INFO),
			format="%(asctime)s %(levelname)s %(message)s",
		)
	except AttributeError:
		logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
		logging.warning("Invalid log level %s, falling back to INFO", args.log_level)

	logging.warning("Video dir : " + str(args.video_dir))

	video_dir = Path(args.video_dir).expanduser().resolve()
	if not video_dir.exists():
		logging.warning("Video directory %s does not exist", video_dir)


	playback = PlaybackController(video_dir)
	player = MQTTVideoPlayer(
		mqtt_host=args.mqtt_host,
		mqtt_port=args.mqtt_port,
		topic_prefix=args.location,
		playback=playback,
		username=args.mqtt_username,
		password=args.mqtt_password,
	)

	# Graceful shutdown on SIGTERM for systemd/launchd usage.
	def _handle_term(_signum, _frame) -> None:
		logging.info("Termination signal received")
		player.shutdown()
		playback.close()
		sys.exit(0)

	signal.signal(signal.SIGTERM, _handle_term)

	try:
		player.run()
	finally:
		playback.close()


if __name__ == "__main__":
	main()

