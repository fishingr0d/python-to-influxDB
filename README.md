# Skrypt python dla bazy danych InfluxDB
 Skrypt pozwalający na pobieranie danych z czujnika, konwetuje je na line protocol, następnie wysyła je do *InfluxDB*.
 
 
## InfluxDB
 [*InfluxDB*](influxdata.com) jest relacyjną bazą danych open source z serii Time Series Database zaprojektowaną z myślą o dużych obciążeniach zapisu i zapytań. Stanowi integralną część tak zwanego [stacka TICK](https://www.influxdata.com/time-series-platform/) (Telegraf, InfluxDB, Chronograf, Kapacitor). Jest to idealna baza danych dla projektów, które generuja duże ilości danych z timestampem. Pozwala na np. monitorowanie czujników IoT i metryk aplikacji.
 Aby móc skorzystać z bazy danych postanowiłam posłużyć się [Dockerem](docker.com). *Docker* jest to otwarte oprogramowanie służące do wizualizacji na poziomie systemu operacyjnego, używane przez programistów i administratorów do tworzenia, wdrażania i uruchamiania aplikacji rozproszonych. Innymi słowami, Docker pozwala nam umieścić program i jego zależności, czyli biblioteki, pliki i konfiguracje w przenośnym, wirtualnym kontenerze. Aby używać Dockera należy zainstalować go ze strony Dockera. 
 Aby zainstalować bazę danych InfluxDB, stworzyłam plik *docker-compose.yml*, w którym zawarłam potrzebne do uzyskania influxa konfiguracje i informację znalezione na [Docker hubie](https://hub.docker.com/_/influxdb).
 
 
### InfluxDB w docker-compose.yml
```
 
version: "3"
services:
    influx:
        image: influxdb
        ports:
            - 8086:8086
        environment: 
            INFLUXDB: Database
            INFLUXDB_ADMIN_USER: admin
            INFLUXDB_ADMIN_PASSWORD: password
            INFLUX_HTTP_AUTH_ENABLED: "true"
            INFLUX_HTTP_FLUX_ENABLED: "true"
        volumes:
            - ./influx:/var/lib/influxdb
        networks:
            admin:
networks:
   admin:
 
```
 
- *image* to obraz, który chcemy wykorzystać w tym przypadku dla influxa jest to *influxdb*
- *ports* tu podajemy port, na którym chcemy, żeby nasz influxdb się znajdował, domślnie jest to ***8086:8086***
- *environment* to "środowisko", w którym będzie działał nasz influx. Zapisujemy tu konfiguracje, na których będzie działał, bez tworzenia pliku konfiguracyjnego.
- *volumes* dyrektywa, która instaluje katalogi źródłowe na komputer lub wewnątrz kontenera. Jeśli ścieżka już istnieje jako część obrazu kontenera, zostanie ona nadpisana w wyznaczonej przez nas ścieżce.


## Grafana
 [*Grafana*](https://grafana.com/) jest to system monitorowania danych z bazy *InfluxDB*, który w czasie rzeczywistym wyświetla dane z bazy danych Influxa, tworząc przy tym różne wykresy. Umozliwia stworzenie *dashboardów*, potrzebnych nam do monitorowania różnych danych, np. możemy monitorować podzespoły naszego komputera. Jeżeli, stweirdzimy, że nasze dashboardy nam się znudziły, *Grafana* oferuje wiele dodatkowych [*pluginów*](https://grafana.com/grafana/plugins) i [*dashboardów*](https://grafana.com/grafana/dashboards), które urozmaicą nam wizualizację naszych danych. Kiedy jesteśmy zajęci i zdala od komputera, w wypadku przekroczenia, danej wartości możemy ustawić **alerty**, kóre będna powiadamiać nas o np. zbyt wysokiej temperaturze procesora. Powiadomienie wsyłane będzie do nas przez różne [*komunikatory dostępne*](https://grafana.com/grafana/#alert-content) dla grafany. Do tego *Grafane* możemy połączyć z wieloma [*bazami danych*](https://grafana.com/grafana/#unify-content).
 
### Grafana w docker-compose.yml

```
grafana:
    image: grafana/grafana:latest
    restart: always
    volumes:
      - ./grafana/:/etc/grafana/
    expose:
      - 3000
    networks:
      - admin

```
 
 
## Chronograf
 [*Chronograf*](https://www.influxdata.com/time-series-platform/chronograf/) działa podobnie jak *Grafana*. Jest to interfejs dla użytkowników i komponent, który pozwala administratorom na wizualizajcę danych z platformy InfluxDB. Można w nim bardzo szybko utworzyć dashboardy z danymi w czasie rzeczywistym, używjąc wybranych templatów lub bibliotek. *Chronograf* podobnie jak *Grafna* oferuje funkcje *alertów*. Jest częścią wcześniej wspomnianego **TICK STACK**'a. 
 Sama obsługa interfejsu *Chronografa* jest bardzo prosta i intuicyjna. Chronograf pozwala nam tworzyć zapytania w dwóch językach ***InfluxQL*** (Influx Query Language), lub w ***Flux***, który domyslnie jest wyłączony. Aby go włącyc należy w pliku konfiguracyjnym *influxdb.conf* znaleźć sekcję zatytułowną **[http]**, następnie znaleźć opcję **flux-enabled = false** i zmienić wartość pola na **"true"**.
  
#### influxdb.conf

```
# ...

[http]

  # ...

  flux-enabled = true

  # ...

```

### Chronograf w docker-compose.yml

```
 chronograf:
    image: chronograf:latest
    ports: 
        - '8888:8888'
    depends_on: 
        - influx
    environment: 
      - INFLUXDB_URL=http://influx:8086
      - INFLUXDB_USERNAME=admin
      - INFLUXDB_PASSWORD=password
    networks:
        admin:

```

# Skrypt Python


## Biblioteki do skryptu Python dla InfluxDB
 Python ma wiele dostępych bibliotek do wykorzystania w naszych projektach, ja użyłam [*PySerial*](https://pythonhosted.org/pyserial/), [*InfluxDBClient*](https://influxdb-python.readthedocs.io/en/latest/api-documentation.html), [*StringIO*](https://docs.python.org/2/library/stringio.html), [*Datetime*](https://docs.python.org/3/library/datetime.html), a z nich wybrałam najpotrzebniejsze **InfluxDBClient, StringIO, datatime**.
 
 ```
 import serial
 from influxdb import InfluxDBClient
 from io import StringIO
 from datetime import datetime
 
```
 
### Konfiguracja InfluxDBClient 

 Następnie stworzyłam zmienną *client*, którą przypisałam do InfluxDBClient i podałam parametry niezbędne mi do połączenia się z moją bazą danych.

```

client=InfluxDBClient(host="localhost",port="8086",username="admin",password="password")
client.create_database("Database")

```
- *host=* jest to parametr, który należy uzupełnić adresem naszej bazy danych, w tym przykładzie to my jesteśmy naszym hostem, więc wpisujemy *"localhost"*.
- *port=* parametr, który wypełniamy portem, na którym znajduje się postawiona przez nas wcześniej baza danych InfluxDB
- *username=* oraz *password=* podajemy nazwę użytkownika i hasło, które podaliśmy przy konfigurowaniu naszej bazy danych

Wywyołujemy naszego *clienta* i tworzymy nową baze danych.

```
client.create_database("DatabasePI")

```

 Następnie tworzymy listę naszych etykiet, którym będziemy przypisywać dane z czujnika i następnie konwertować do *line protocol* naszej bazy danych.

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
client.write_points(data,time_precision='s',database='Database', protocol='line')
    print(data)
```
