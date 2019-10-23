from flask import Flask
from flask import request
from flask import Response
from flask import jsonify

import paho.mqtt.client as mqtt

app = Flask(__name__)

topic = 'foo'
topic2 = 'bar'
port = 5000

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    client.publish(topic2, "STARTING SERVER")
    client.publish(topic2, "CONNECTED")
    print("Connected")


def on_message(client, userdata, msg):
    client.publish(topic2, "MESSAGE")

def on_log(client, userdata, level, buf):
    print("log: ",buf)

@app.route('/')
def hello_world():
    return 'Hello World new! I am running on port ' + str(port)


@app.route('/mqtt/api/pub/<topic>', methods=['GET'])
def pub_topic(topic):
    client.publish(topic, "MSG")
    return topic


@app.route('/mqtt/api/publish', methods=['POST', 'OPTIONS'])
def create_task():
    if request.method == 'POST':
        if not request.json or not 'title' in request.json:
            abort(400)
        print("post")
        client.publish(request.json['title'], "MSG")
        resp = Response(request.json['title'])
        #jsonify(title='test')) 
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp
    resp = Response('test')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp


if __name__ == '__main__':
    print("Starting Flask with MQTT Client...")
    client = mqtt.Client("FlaskMQTTClient")
    client.on_log=on_log

    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('localhost')
    client.loop_start()

    app.run(host='0.0.0.0', port=port)

