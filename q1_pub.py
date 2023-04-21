import sys
import time
import paho.mqtt.client as mqtt
import Adafruit_DHT

channel_id = "2099029"
username = "DS0NAiwRAis5HTUpMR09BRo"
password = "P+cMvDo4uJJoBipUWIoeLRSL"
pub_topic = "channels/"+channel_id+"/publish"

client = mqtt.Client(client_id=username, transport="websockets")
client.username_pw_set(username, password)

client.connect("mqtt3.thingspeak.com", 80)

def sendData():
    try:
        hum, temp = Adafruit_DHT.read_retry(11, 4)
        data = "field1="+str(temp)+"&field2="+str(hum)+"&status=mqttpublish"
        print(data)
        val = client.publish(topic=pub_topic, payload=data)
        print(val)
    except Exception as e:
            print("connection error: ", e)


if __name__ == "__main__":
    while True:
        sendData()
        time.sleep(1)