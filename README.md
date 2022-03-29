# Projet-Designed

Welcome to this project combining Apache Kafka, Kafka Connect and MongoDB.

The goal of this project is to work on the Binance API to get data. 

In this project, the notebook **ProjectApache.ipynb** contains the core of the project. Here we fill a file with the data received via a python file and put it in the form of a text file. 

Then, with Kafka we put them in our topics and from there, Kafka Connect links with the MongoDB database. We then perform queries on the database. 

The last cell of the notebook contains an interactive menu, allowing you to choose to fill the topics (and subsequently the database), to perform the MongoDB queries (this part contains a sub-menu allowing you to select certain queries) and finally to leave the menu.

Depending on your connection, it takes about **1 min - 2 min** to make the calls via the Binance API and to fill the topic, with each call the data changes to have the latest data.

Also, if you see this line: **Output exceeds the size limit. Open the full output data in a text editor**, to display the data you need to click on **in a text editor** to display it afterwards.

# Usage of the script

## First (it depends on your config or/and OS)

Launch : MongoDB

```bash
mongo --host 127.0.0.1:27017
```
Launch : Zookeeper

```bash
zookeeper-server-start.sh config/zookeeper.properties
```
Launch : Kafka

```bash
kafka-server-start.sh config/server.properties
```
And for display the data of the topic :

```bash
bin/kafka-console-consumer.sh --topic ApiBinance --from-beginning --bootstrap-server localhost:9092
```
## Name of Topic and Databse 

For MongoDB :

Our database is called **"Binance"** and our collection is called **"symbol"**.

For Kafka :

Our Topic is called **"ApiBinance"**.

## Setting up

Then, import (or install) this for the notebook (already in the notebook) :

```py
from kafka import KafkaProducer, KafkaConsumer
from time import sleep
import json
from datetime import datetime
from confluent_kafka import Producer
from pymongo import MongoClient, ASCENDING, DESCENDING
from pprint import pprint
from itertools import combinations, combinations_with_replacement
from kafka.admin import KafkaAdminClient, NewTopic
from EtudeBinance import getpairs
```

Then, import (or install) this for **EtudeBinance.py** (already in **EtudeBinance.py**) :

```py
import requests
from datetime import *
import time
from itertools import combinations, combinations_with_replacement
```

# Finally

You need to use three files, the jupyter notebook **ProjectApache.ipynb**, **fichier.txt** (the file which contains the data of EtudeBinance.py) and **EtudeBinance.py**, you need to put this three files in the same directory and for **EtudeBinance.py** (when you see this line) :  

```py
%run '/home/souhail/Documents/Designed Distributed Systems/EtudeBinance.py'
```

**Change it by your full path (the path of EtudeBinance.py).**

If you can't find your full path to the file you can delete this line and use only the text file (**In this case, you will not have access to the data renewal**).

**The project is carried out in collaboration with <a href="https://github.com/martinmouly" target="_blank">Martin MOULY</a> et <a href="https://github.com/Pierregvx" target="_blank">Pierre GUEVENEUX</a> within the Designing Distributed Systems project.**
