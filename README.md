# Skrypt python dla bazy danych InfluxDB
Opis jakiś co robi skrypt.

## Biblioteki do skryptu Python dla InfluxDB
Python ma wiele dostępych bibliotek do wykarzystania w naszych projektach, ja użyłam *serial, influxdb, io, datatime, pandas*, a z nich wybrałam najpotrzebniejsze *InfluxDBClient, StringIO, datatime*.

```
 import serial
 from influxdb import InfluxDBClient
 from io import StringIO
 from datetime import datetime
 import pandas as pd
 
```
### Konfiguracja InfluxDBClient 

Następnie stworzyłam zmienną *client*, którą przypisałam do InfluxDBClient i podałam parametry niezbędne mi do połączenia się z moją bazą danych.

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
### Konfiguracja PySerial
Kolejnym krokiem jest dodanie zmeinnej dla naszego czujnika i przypisania mu jego parametrów.
```
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.flushInput()
```
*ser.flushInput()* odpowiada za opróżnianie bufforu z całej jego zawarotści.

### Pętla tworząca protocol line

Tworzymy pętlę, która nigdy nie spełni warunku, więc nigdy nie przestanie wykonywać instrukcji, które są w niej zapisane. 
Dane z czujnika wczytujemy do zmiennej x. Następnie tworzymy zmienną *now*, która po skonwertowaniu na zmienną *int* oraz później na zmienną *string* będzie naszym timestampem, czyli będzie to czas, októrym dane te zostay wysłane na serwer. Rozdzielamy nasze dane znakakami **" , "** oraz **" ' "** i konwertujemy je na *String*. Dane wrzucamy do naszej tablicy, w kolejnej pętli tworzymy nasz protocol line, kótóry pozwala nam dodać dane do bazy danych. Dodajemy ***measuremen*** ***etykietę*** zgodną z licznikiem naszej pętli oraz ***jedną wartość z tablicy***, na końcu dopisując ***timestampa***. Gotową linijkę dodajemy do naszej tablicy za pomocą instrukcji ***data.appeand(new_line)***.

```

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
```
### Ostatni krok, dodawanie danych do bazy InfluxDB

 Odnosząc się do naszej zmiennej klienta InfluxDBClient, którą stworzylismy na samym początku dodajemy ***write_points*** oraz wpisujemy potrzebne nam parametry.
 Następnie dla własnej wiedzy wyświetlam w terminalu lineprotocol, którym dodaję dane do Influxa. 

```
client.write_points(data,time_precision='s',database='DatabasePI', protocol='line')
    print(data)
```
