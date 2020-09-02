# Skrypt python dla bazy danych InfluxDB
Opis jakiś co robi skrypt.
## Skrypt Python
Python ma wiele dostępych bibliotek do wykarzystania w naszych projektach, ja użyłam *serial, influxdb, io, datatime, pandas*, a z nich wybrałam najpotrzebniejsze *InfluxDBClient, StringIO, datatime*.

```
 import serial
 from influxdb import InfluxDBClient
 from io import StringIO
 from datetime import datetime
 import pandas as pd
 
```
Następnie stworzyłam klasę *client*, którą przypisałam do InfluxDBClient i podałam parametry niezbędne mi do połączenia się z moją bazą danych.

```

client=InfluxDBClient(host="localhost",port="8086",username="admin",password="pass")
client.create_database("DatabasePI")

```
- *host=* jest to parametr, który należy uzupełnić adresem naszej bazy, w tym przykładzie jest to my jesteśmy naszym hostem, więc wpisujemy *"localhost"*.
- *port=* to parametr, który wypełniamy portem, na którym znajduje się postawiona przez nas wcześniej baza danych InfluxDB
- *username=* oraz *password=* podajemy nazwę użytkownika i hasło, które podaliśmy przy konfigurowaniu naszej bazy danych

Wywyołujemy naszego *clienta* i tworzymy nową baze danych

```
client.create_database("DatabasePI")

```

Następnie tworzymy listę naszych etykiet, którym będziemy przypisywać dane z czujnika i następnie konwertować do *lineprotocol* naszej bazy danych

```
etykiety = ["temperatura=",
            "napiecie=",
            "prad_ladowania=",
            "pojemosc="]
```

Kolejnym krokiem jest dodanie klasy dla naszego czujnika i przypisania mu parametrów.
```
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
```

**
