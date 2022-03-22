import pymongo

from pymongo import MongoClient, ASCENDING, DESCENDING

from pprint import pprint


client = MongoClient("localhost", 27017)

mydatabase = client.mesclients

mycollection = mydatabase.clients

#print(mycollection.find().pretty())

for i in mycollection.find():
    print(i)
print(mydatabase.clients.count_documents({}))

cursor = mycollection.find({})
for document in cursor: 
    pprint(document)


#Exercice 1

#Step 1 :

mydb = client.mydatabase
collection = mydb.employee
mydb.employee.delete_many({})
#collection.create_index("ID", unique = True)
#collection.create_index("ID")
#esp = collection.create_index([ ("field_to_index", ASCENDING) ])

try:
    emp_rec1 = {
            "ID":1,
            "Civility":"Mr",
            "name":"Geek",
            "adress":"Paris",
            "location":15000,
            }
    emp_rec2 = {
            "ID":2,
            "Civility":"Mr",
            "name":"Shaurya",
            "adress":"Paris",
            "salary":1400,
            }

    emp_rec3 = {
            "ID":3,
            "Civility":"Mme",
            "name":"Pokee",
            "adress":"Delhi",
            "location":1120,
            }
    emp_rec4 = {
            "ID":4,
            "Civility":"Mme",
            "name":"Soso",
            "adress":"Bezons",
            "salary":1700,
            }

    emp_rec5 = {
            "ID":5,
            "Civility":"None",
            "name":"David",
            "adress":"Amsterdam",
            "location":10000,
            }
    emp_rec6 = {
            "ID":6,
            "Civility":"None",
            "name":"Alpha",
            "adress":"Tokyo",
            "salary":1460,
            }
    
    # Insert Data
    rec_id1 = collection.insert_one(emp_rec1)
    rec_id2 = collection.insert_one(emp_rec2)
    rec_id1 = collection.insert_one(emp_rec3)
    rec_id2 = collection.insert_one(emp_rec4)
    rec_id1 = collection.insert_one(emp_rec5)
    rec_id2 = collection.insert_one(emp_rec6)
    print("Data inserted with record ids",rec_id1," ",rec_id2)
except:
    print("Deja fait")
  
# Printing the data inserted
cursor = collection.find()
for record in cursor:
    print('yo',record)


db = client.Binance
collection = db.symbol
db.symbol.delete_many({})
emp_rec1 = {
            "ID":1,
            "Civility":"Mr",
            "name":"Geek",
            "adress":"Paris",
            "location":15000,
            }
nom={
        "ID": 1, 
        "symbol": "ETHBTC", 
        "priceChangePercent": 0.654
        }
nom2={
        "ID": 2, 
        "symbol": "BTCUSDT", 
        "priceChangePercent": 2.976
        }
rec_id1 = collection.insert_one(nom)
rec_id2 = collection.insert_one(nom2)