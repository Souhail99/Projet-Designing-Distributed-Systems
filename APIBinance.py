import requests
import json
import sqlite3
from datetime import *
import hmac
import hashlib

#region tools
#/api/v3/exchangeInfo

bdd="BPtrading.db"

#region  endpoints
listPair = "/api/v3/ticker/price"
baseapi="https://api.binance.com"
listpricebook="/api/v3/ticker/bookTicker"
orderbook = "/api/v3/depth"
candle = "/api/v3/klines"
recentTrades = "/api/v3/trades"
Alltrades="/api/v3/historicalTrades"
#endregion

api_key="BeASbgT7Ti3qs09RMKRLJqb69aCjkSaMhBkOlZAHdxRJfnXhqXj0inA2S1pEpSW4"
secret_key="b0dhGlnqjFyE8xgXaBoTbGSGgXPqnyXgRGnqaH3neKYR2mQIv1L9RlJpRZ6f4NTW"

#region get dict from the api (from the json)
def getdic(endpoint:str,param:dict={}):
    r=requests.get(baseapi+endpoint,params=param)
    liste=r.json()
    return liste
#endregion

#region get cryptos
def getpairs():
    liste=getdic(listPair)
    paires = [""]
    for i in liste:
        pair = i["symbol"]
        paires.append(pair)
    return paires


def allcrypto():
    toremove4 = ["BUSD","USDT","USDC","TUSD"]
    toremove3 = ["BTC","BNB","ETH","TRY","BRL"]
    cryptolist = [""]
    liste = getpairs()
    for symb in liste:
        if symb[:len(symb)-3] not in cryptolist and symb[:len(symb)-4] not in cryptolist:
            if symb[len(symb)-3:] in toremove3:
                symb= symb[:len(symb)-3]
            elif symb[len(symb)-4:] in toremove4:
                symb= symb[:len(symb)-4]
            else:
                print("paire à ajouter : ",symb,"\n")
            cryptolist.append(symb)
    return cryptolist
#endregion


#region orderbook analysis
def getDepth(direction:str,symbol:str):
    dic ={'bid':'bidPrice','ask':'askPrice'}
    info ={}
    for u in getdic(listpricebook):
        if u["symbol"]==symbol :
            info =u
    return info[dic[direction]]

#returns the order book of the pair for a period of time in minutes
def orderbooklists(symbol:str,limit=10):
    return getdic(orderbook,{"symbol":symbol,"limit":limit})
#endregion



#region candle
#region possible intervals
"""1m
3m
5m
15m
30m
1h
2h
4h
6h
8h
12h
1d
3d
1w
1M"""
#endregion
#endregion

#region alldata
#Refresh Data
def refreshData(symbol:str):
    headers = {
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': api_key
    }
    r = requests.get(baseapi + "/api/v3/historicalTrades?symbol=" + symbol,headers=headers)
    print(r.json()[0])
    liste=r.json()
    for dico in liste:
        dico["side"] = "buyer_and_" if dico["isBuyerMaker"] == True else "seller_and_"
        dico["side"] += "best match" if dico["isBestMatch"] == True else "not_best_match"

        del dico["isBuyerMaker"]
        del dico["isBestMatch"]
    return liste

#The function allow us to know the candle available after the last one in our database, or return in one interval the candle if you don't put a startime or an endtime
def refreshDataCandle(pair:str,startime=None,endtime=None,interval="1m"):
    if endtime==None:
        r = requests.get(baseapi+ "/api/v3/klines?symbol=" + pair +"&interval=" +interval)
        listes=r.json()
    else:
        r = requests.get(baseapi+ "/api/v3/klines?symbol=" + pair +"&interval=" +interval +"&startTime="+ str(startime)+ "&endTime=" +str(endtime))
        listes=r.json()
    return StoreDataCandle(listes)



#rthis function is useful to return in the good order for refreshdata et refreshdatacandle
def StoreDataCandle(listes:list):
    listes=listes
    #print(listes)
    storage=[]
    for i in listes:
        #print(i)
        storage.append(i[0])
        storage.append(i[2])
        storage.append(i[3])
        storage.append(i[1])
        storage.append(i[4])
        storage.append(i[5])
    return storage

### avoir init storage to write in our database
pair='ETHUSDT'
storage=refreshDataCandle(pair)
storagefulldata =refreshData(pair)
###
#we first called candle modify then StorageOfDataCandle
#The candlModify useful to know the last  candle and return the currently available one
def candlModify(database:str,pairtosync:str):
    con = sqlite3.connect(database)
    query = "SELECT date FROM candles"+pairtosync
    cur = con.cursor()
    cur.execute(query)
    j=cur.fetchall()
    start_time=int(j[len(j)-1][0])
    print("endtime", start_time)
    con.commit() 
    con.close()
    timeactuelle=datetime.now().timestamp()
    end_time = int(timeactuelle) * 1000
    start_time = start_time * 1000
    storage=refreshDataCandle(pair,start_time,end_time)
    del storage[0]
    return storage


#region write with sqlite to have a database
def StorageOfDataCandle(pair:str,storage):
    try:
        name="candles"+pair
        con = sqlite3.connect(bdd)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+name+"';")
        variable=cur.fetchone()
        if variable==None:
        # Create table
            cur.execute('''CREATE TABLE  candles'''+pair+''' 
                        (Id integer primary key, date int, high real, low real, open real, close real, volume real)''')  
            print("========================================")
            j=0
            submit = ""       
            for i in range(0,len(storage)-1,6):
                submit += "INSERT INTO candles"+pair+" VALUES ("+str(j)+","+str(int(int(storage[i])/1000))+","+ str(float(storage[i+1]))+","+ str(float(storage[i+2]))+","+ str(float(storage[i+3]))+","+ str(float(storage[i+4]))+","+ str(float(storage[i+5]))+");" + "\n"
                j+=1
            con.executescript(submit)
        else:
            cur.execute("select count(*) from candles"+pair+";")
            j=cur.fetchone()[0]
            print(j)
            submit = ""       
            for i in range(0,len(storage)-1,6):
                submit += "INSERT INTO candles"+pair+" VALUES ("+str(j)+","+str(int(int(storage[i])/1000))+","+ str(float(storage[i+1]))+","+ str(float(storage[i+2]))+","+ str(float(storage[i+3]))+","+ str(float(storage[i+4]))+","+ str(float(storage[i+5]))+");" + "\n"
                j+=1
            print(submit)
            con.executescript(submit)
        print("Success !")
    except:
        print("Erreur d'enrigistrement")
    
    for row in con.execute("select * from candles"+pair):
        print(row)
    cur.execute("select count(*) from candles"+pair+";")
    print(cur.fetchone()[0])
    con.commit()
   
    con.close()

    
def StorageOfFull(pair:str,storagefulldata):
    try:
        name="FulldataSet"
        con = sqlite3.connect(bdd)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+name+"';")
        variable=cur.fetchone()
        print(variable==None)
        if variable==None:
        # Create table
            cur.execute('''CREATE TABLE  FulldataSet'''+""+''' 
                        (Id integer primary key, uuid text, traded_crypto text, price real, created_at_int int, side text)''')  
            
            print("========================================")
            j=0
            submit = ""       
            for i in storagefulldata:
                submit += "INSERT INTO FulldataSet VALUES ("+str(j)+",'"+str(int(i['id']))+"','"+ str(pair)+"',"+ str(float(i['price']))+","+ str(int(i['time']))+",'"+i['side']+"');" + "\n"
                j+=1
            print(submit)
            con.executescript(submit)
        else:
            cur.execute("select count(*) from FulldataSet"+";")
            j=cur.fetchone()[0]
            print(j)
            submit = ""       
            for i in storagefulldata:
                submit += "INSERT INTO FulldataSet VALUES ("+str(j)+",'"+str(int(i['id']))+"','"+ str(pair)+"',"+ str(float(i['price']))+","+ str(int(i['time']))+",'"+i['side']+"');" + "\n"
                j+=1
            con.executescript(submit)
        
    except:
        print("Erreur d'enregistrement")
    
    for row in con.execute("select * from FulldataSet"):
        print(row)
    cur.execute("select count(*) from FulldataSet ;")
    print(cur.fetchone()[0])
    con.commit()
    con.close()
#endregion





#region Post-Order

def getdicpost(endpoint:str,param:dict={},headers:dict={}):
    r=requests.post(baseapi+endpoint,params=param,headers = headers)
    liste=r.json()
    return liste
def makeOrder(symbol,side,type,timeInForce,quantity,price,):
    timestamp=datetime.now().timestamp()
    timestamp = int(timestamp) * 1000
    requete = "symbol="+symbol+"&side="+side+"&type="+type +"&timeInForce="+timeInForce+"&quantity="+quantity+ "&price="+price+ "&timestamp="+str(timestamp)
    signature = hmac.new(secret_key.encode('utf-8'), requete.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Content-Type': 'application/json','X-MBX-APIKEY': api_key}
    r = requests.post(baseapi + "/api/v3/order?"+ requete+ "&signature="+signature,headers=headers)
    print(r.json())
    return r.json()

def cancelOrder(symbol,orderId):
    timestamp=datetime.now().timestamp()
    timestamp = int(timestamp) * 1000
    requete = "symbol="+symbol+"&orderId="+str(orderId)+"&timestamp="+str(timestamp)
    signature = hmac.new(secret_key.encode('utf-8'), requete.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Content-Type': 'application/json','X-MBX-APIKEY': api_key}
    r=requests.delete(baseapi+"/api/v3/order?"+requete+"&signature="+signature,headers=headers)
    print(r.text)
#cancelOrder("BANDUSDT",makeOrder('BANDUSDT','SELL','LIMIT','GTC','1.7','6')["orderId"])
#create an order and cancell it right away




def MakeaConnection():

    return 5





#region main
if __name__ == '__main__':
    print(getdic())
    #print(allcrypto())
    #print(getDepth("ask","ETHUSDT"))
    #orderbooklists("BTCUSDT")

    #StorageOfDataCandle(pair,storage)
    #StorageOfDataCandle(pair,candlModify(bdd,pair))
    #StorageOfFull(pair,storagefulldata)

    #cancelOrder("BANDUSDT",makeOrder('BANDUSDT','SELL','LIMIT','GTC','1.7','6')["orderId"])
#endregion
