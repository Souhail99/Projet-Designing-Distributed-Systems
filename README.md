# Projet-Designed

Bienvenue pour ce projet alliant Apache Kafka, Kafka connect et MongoDB.

Le but de ce projet est de travailler sur l'api Binance pour obtenir des données. Dans ce projet, le notebook **ProjectApache.ipynb** contient le coeur du projet. Ici, nous remplissons un fichier composé des données reçu puis avec kafka nous les mettons dans nos topics et ensusite kafka connect fait le lien avec la database MongoDB. Nous réalisons ensuite des requêtes sur la database. 

La dernière cellule du Notebook contient un menu interactif, vous laissant au choix de remplir les topics (et par la suite la database), d'effectuer les requêtes mongoDB (cette partie contient un sous-menu vous permettant de sélectionner certaines requêtes) et efin de quitter le menu.

Selon votre connexion, il faut environ 1min pour réaliser les appels via l'api Binance et pour remplir le topic.

Aussi, si vous voyez cette ligne : **Output exceeds the size limit. Open the full output data in a text editor**, pour afficher les données vous devez cliquer sur **in a text editor**.

## Usage of the script

# First (it depends on your config and OS)

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

You to use three files, the jupyter notebook **ProjectApache.ipynb**, **fichier.txt** (the file which contains the data of EtudeBinance.py) and **EtudeBinance.py**, you need to put this three files in the same directory and for **EtudeBinance.py** (when you see this line) :  

```py
%run '/home/souhail/Documents/Designed Distributed Systems/EtudeBinance.py'
```
**Change it by your full path (the path of EtudeBinance.py)**

**Le projet est effectué en collaboration avec <a href="https://github.com/martinmouly" target="_blank">Martin MOULY</a> et <a href="https://github.com/Pierregvx" target="_blank">Pierre GUEVENEUX</a> dans le cadre du projet Designed Distributed Systems**
