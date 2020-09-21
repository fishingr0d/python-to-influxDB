#!/usr/bin/env python
import serial
from influxdb import InfluxDBClient
from io import StringIO
from datetime import datetime
import pandas as pd

client=InfluxDBClient(host="localhost",port="8086",username="admin",password="password")
client.create_database("DatabasePI")

etykiety = ["temperatura=",
            "napiecie=",
            "prad_ladowania=",
            "pojemosc="]

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.flushInput()
while 1:
    x=ser.readline()
    now = datetime.now()
    timestamp = str(int(datetime.timestamp(now)))
    splitted=str(x.split()[0])
    y = splitted.split("'")[1]
    y = y.split(",")
    data=[]
    
    for i in range(0,len(y)):
        new_line = "measurement " + etykiety[i] + y[i] + " " + timestamp
        data.append(new_line)

    client.write_points(data,time_precision='s',database='DatabasePI', protocol='line')
    print(data)
       
    
