import paho.mqtt.client as mqtt
import tkinter as tk
import json

broker = "mqtt3.thingspeak.com"
port= 80
username = "IS80BhspGwIlMjMbIwsfNiY"
clientId = "IS80BhspGwIlMjMbIwsfNiY"
password = "64zaWOjeHbKdc4PAC0+RlLOw"

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Successfully connected to MQTT broker")
        status_label.config(text=f"Successfully connected to MQTT broker")
    else:
        print("Failed to connect, return code %d", rc)
        status_label.config(text=f"Failed to connect to MQTT broker")


def on_subscribe(client, userdata, mid, granted_qos):
    channelId = channelId_entry.get()
    print("Subscribed! woah!")
    status_label.config(text=f"Connected & Subscribed to channel {channelId}")

def on_message(client, userdata, message):
    msg = json.loads(message.payload.decode('ascii'))
    timestamp = msg['created_at']
    temperature = msg['field1']
    humidity = msg['field2']

    sensor_data_text.config(state=tk.NORMAL)
    sensor_data_text.insert(tk.END, f"{timestamp}  Temp: {temperature}  Humidity: {humidity}\n")
    sensor_data_text.config(state=tk.DISABLED)

client = mqtt.Client(client_id=clientId, transport="websockets")
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

def subscribe():
    channelId = channelId_entry.get()
    client.connect(broker, port)
    
    sub_topic = "channels/"+str(channelId)+"/subscribe"
    client.loop_start()

    client.subscribe(topic=sub_topic, qos = 0)

root = tk.Tk()
root.title("MQTT Subscribe")
root.minsize(300, 300)

channelId_entry = tk.Label(root, text="Channel Id")
channelId_entry.grid(row=1, column=0, columnspan=2,padx=5, pady=5)

channelId_entry = tk.Entry(root)
channelId_entry.grid(row=1, column=1,columnspan=1,  padx=5, pady=5,)


connect_button = tk.Button(root, text="Subscribe", command=subscribe)
connect_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

sensor_data_text = tk.Text(root, height=20, width=100, background='grey')
sensor_data_text.grid(row=5, column=0, padx=5, pady=5, columnspan=2)
sensor_data_text.config(state=tk.DISABLED)

root.mainloop()





