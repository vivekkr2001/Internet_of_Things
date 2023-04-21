import time
import Adafruit_DHT
import mysql.connector
import tkinter as tk
import datetime 
import threading

myDb = mysql.connector.connect(
    host="127.0.0.1", user="19mcme18", password="passwd@123", database="19mcme18")
sql = "CREATE DATABASE IF NOT EXISTS 19mcme18"
myCursor = myDb.cursor()
myCursor.execute(sql)
tableSql = "CREATE TABLE IF NOT EXISTS data1 (timestamp timestamp, temperature double, humidity double)"
myCursor.execute(tableSql)


def readAndStore():
    def updateTable(temperature, humidity):
        insertSql = "INSERT INTO data1(temperature, humidity) VALUES ("+ str(
            temperature) + ","+str(humidity) + ")"
        myCursor.execute(insertSql)
        myDb.commit()
    try:
        hum, temp = Adafruit_DHT.read_retry(11, 4)
        data = "field1="+str(temp)+"&field2="+str(hum)
        print(data)
        hum, temp = Adafruit_DHT.read_retry(11, 4)
        data = "field1="+str(temp)+"&field2="+str(hum)
        print(data)
        now = datetime.datetime.now()
        if temp is not None and hum is not None:
            updateTable(format(temp, '.2f'), format(hum, '.2f'))
        else:
            updateTable(0.0, 0.0)
        
        sensor_data_text.config(state=tk.NORMAL)
        sensor_data_text.insert(tk.END, f"DHT11, {now}, Temperature: {temp}°C, Humidity: {hum}\n")
        sensor_data_text.config(state=tk.DISABLED)
        time.sleep(1)
    except Exception as e:
        print("connection error: ", e)

root = tk.Tk()
root.title("Sensor Data Collection")
root.minsize(300,300)

sensor_data_text = tk.Text(root, height=10, width=50)
sensor_data_text.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
sensor_data_text.config(state=tk.DISABLED)

refresh_button = tk.Button(root, text="Read And Store", command=readAndStore)
refresh_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
