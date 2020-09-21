# Skrypt python dla bazy danych InfluxDB
 Skrypt pobiera dane z czujnika, konwetuje je na line protocol, następnie wysyła je do Influxa.
 
## InfluxDB w Docker
 *InfluxDB* jest relacyjną bazą danych open sourcew z serii Time Series Database zaprojektowaną z myślą o dużych obciążeniach zapisu i zapytań. Stanowi integralną część tak zwanego stacka TICK (Telegraf, InfluxDB, Chronograf, Kapacitor). Jest to idealna baza danych dla projektów, które generuja duże ilości danych z timestampem. Pozwala na np. monitorowanie czujników IoT i metryk aplikacji.
 Aby móc korzystac z bazy danych postanowiłam posłuzyc sie Dockerem. *Docker* jest to otwarte oprogramowanie służące do wizualizacji na poziomie systemu operacyjnego, używane przez programistów i administratorów do tworzenia, wdrażania i uruchamiania aplikacji rozproszonych. Innymi słowami, Docker pozwala nam umieścić program i jego zależności, czyli biblioteki, pliki i konfiguracje w przenośnym, wirtualnym kontenerze. Aby uzywać Dockera należy zainstalować go ze strony Dockera
 Aby zainstalować bazę danych InfluxDB, stworzyłam plik *docker-compose.yml*, w którym zawarłam potrzebne do uzyskania influxa konfiguracje i informację  znalezione na docker
 
 '''
 
version: "3"
services:
    influx:
        image: influxdb
        ports:
            - 8086:8086
        environment: 
            INFLUXDB: DatabasePI
            INFLUXDB_ADMIN_USER: INFLUXDB_ADMIN_USER
            INFLUXDB_ADMIN_PASSWORD: pass
            INFLUX_HTTP_AUTH_ENABLED: "true"
            INFLUX_HTTP_FLUX_ENABLED: "true"
        volumes:
            - ./influx:/var/lib/influxdb
        networks:
            admin:
networks:
   admin:
 
 '''
 
 *image* to obraz, z który chcemy wykorzystać w tym przypadku dla influxa jest to *influxdb*
 *ports* tu podajemy port, na którym chcemy, żeby nasz influxdb siś znajdował, domślnie jest to ***8086:8086***
 *environment* to "środowisko", w którym będzie działał nasz influx. Zapisujemy tu konfiguracje, na których będzie działał, bez tworzenia pliku konfiguracyjnego.
*volumes* durektywa, która instaluje katalogi źródłowe na komputer lub wewnątrz konternera. Jeśli ścieżka już istnieje jako częśc obrazu kontenera, zostanie ona nadpisana przez wyznaczona przez nas ścieżkę.
 

## Biblioteki do skryptu Python dla InfluxDB
 Python ma wiele dostępych bibliotek do wykorzystania w naszych projektach, ja użyłam *serial, influxdb, io, datatime, pandas*, a z nich wybrałam najpotrzebniejsze *InfluxDBClient, StringIO, datatime*.

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

client=InfluxDBClient(host="localhost",port="8086",username="admin",password="password")
client.create_database("DatabasePI")

```
- *host=* jest to parametr, który należy uzupełnić adresem naszej bazy, w tym przykładzie jest to my jesteśmy naszym hostem, więc wpisujemy *"localhost"*.
- *port=* to parametr, który wypełniamy portem, na którym znajduje się postawiona przez nas wcześniej baza danych InfluxDB
- *username=* oraz *password=* podajemy nazwę użytkownika i hasło, które podaliśmy przy konfigurowaniu naszej bazy danych

Wywyołujemy naszego *clienta* i tworzymy nową baze danych

```
client.create_database("DatabasePI")

```

 Następnie tworzymy listę naszych etykiet, którym będziemy przypisywać dane z czujnika i następnie konwertować do *line protocol* naszej bazy danych

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
Dane z czujnika wczytujemy do zmiennej x. Następnie tworzymy zmienną *now*, która po konwertujemy na zmienną typu *int* oraz później na zmienną typu *string* będzie naszym timestampem, czyli będzie to czas, w którym dane te zostay wysłane na serwer. Rozdzielamy nasze dane znakakami **" , "** oraz **" ' "** i konwertujemy je na *String*. Dane wrzucamy do naszej tablicy, w kolejnej pętli tworzymy nasz protocol line, kótóry pozwala nam dodać dane do bazy danych. Dodajemy ***measuremen*** ***etykietę*** zgodną z licznikiem naszej pętli oraz ***jedną wartość z tablicy***, na końcu dopisując nasz ***timestamp***. Gotową linijkę dodajemy do naszej tablicy za pomocą instrukcji ***data.appeand(new_line)***.

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
