import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as sub
import paho.mqtt.publish as pub

channel_id = 2099029
broker = "mqtt3.thingspeak.com"
port= 80
write_api = "PBHIXPS6NETXOUXB"
read_api = "J7O2Q1BFHE0YTVXP"
username = "IS80BhspGwIlMjMbIwsfNiY"
password = "64zaWOjeHbKdc4PAC0+RlLOw"

pub_topic = "channels/2099029/publish"
pub_payload = "field1=45&field2=60&status=MQTTPUBLISH"

sub_topic = "channels/2099029/subscribe"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Successfully connected to MQTT broker")
    else:
        print("Failed to connect, return code %d", rc)

def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

client = mqtt.Client(client_id="IS80BhspGwIlMjMbIwsfNiY", transport="websockets")
client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_message = on_message
client.cleanSession = True
client.connect(broker, port)
client.publish(topic=pub_topic, payload=pub_payload)
    
client.subscribe(topic=sub_topic, qos = 1)

client.loop_forever()

