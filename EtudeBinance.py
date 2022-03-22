import requests
import sqlite3
from datetime import *
import time
from itertools import combinations, combinations_with_replacement

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

#region tools
#/api/v3/exchangeInfo

bdd="BPtrading.db"
baseapi="https://api.binance.com"
listpricebook="/api/v3/ticker/bookTicker"

#region  endpoints
listPair = "/api/v3/ticker/price"

orderbook = "/api/v3/depth"
candle = "/api/v3/klines"

recentTrades = "/api/v3/trades"
Alltrades="/api/v3/historicalTrades"
CurrentAveragePrice="/api/v3/avgPrice"
PriceChangeStatistics="/api/v3/ticker/24hr" #24hr Ticker Price Change Statistics
#endregion

api_key="BeASbgT7Ti3qs09RMKRLJqb69aCjkSaMhBkOlZAHdxRJfnXhqXj0inA2S1pEpSW4"
secret_key="b0dhGlnqjFyE8xgXaBoTbGSGgXPqnyXgRGnqaH3neKYR2mQIv1L9RlJpRZ6f4NTW"



def Latestprice(endpoint:str,param:dict={}):
    r=requests.get(baseapi+endpoint,params=param)
    liste=r.json()
    return liste

def candles(endpoint:str,param:dict={}):
    r=requests.get(baseapi+endpoint,params=param)
    liste=r.json()
    return liste

def PriceChange(endpoint:str,param:dict={}):
    r=requests.get(baseapi+endpoint,params=param)
    liste=r.json()
    return liste

def CurrentAveragePrices(endpoint:str,param:dict={}):
    r=requests.get(baseapi+endpoint,params=param)
    liste=r.json()
    return liste

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



#region Post-Order

def getdicpost(endpoint:str,param:dict={},headers:dict={}):
    r=requests.post(baseapi+endpoint,params=param,headers = headers)
    liste=r.json()
    return liste


def Makethefile(symboles,Allsymboles):
    inexistant=[]
    compteur=1
    with open("fichier.txt", "w") as file:
        for symbol in symboles:
            if symbol in Allsymboles:
                dic2={'symbol':symbol}
                js=PriceChange(PriceChangeStatistics,dic2)
                keys = list(js.keys())
                index=[]
                for i in range(len(keys)):
                    if i == 0 or i == 2 or i == 5 or i== 6 or i == 12 or i == 13 or i == 14:
                        index.append(keys[i])
                file.write("{")
                file.write('"'+"ID"+'"'+":"+" "+str(compteur)+", ")
                compteur+=1
                for i in range(len(index)):
                    symbol=js[index[0]]
                    boole=False
                    try:
                        float(js[index[i]])
                        boole=True
                    except:
                        boole=False

                    if boole!=True:
                        file.write('"'+index[i]+'"'+":"+" "+'"'+js[index[i]]+'"'+", ")
                    else:
                        file.write('"'+index[i]+'"'+":"+" "+str(js[index[i]])+", ")
                dic2={'symbol':symbol}
                alpha=CurrentAveragePrices(CurrentAveragePrice,dic2)
                file.write('"'+str('currentaverageprice')+'"'+":"+" "+alpha['price'])
                file.write("},WEEE")
            else:
                inexistant.append(symbol)
    print("Les symboles inexistant dans la liste : ",inexistant)








#region main
if __name__ == '__main__':
    symboles=list(filter(('').__ne__, getpairs()))
    new=[]
    #print(allcrypto())
    listesymboles=["BTC","ETH","USDT","USD","BNB","XRP","ADA","DOGE","LTC","BCH","SOL","ETC","LUNA","AVAX","SHIB","DOT","MATIC","AAVE","UNI","VRA","USDC","ADX","USDC","APE","JASMY","GALA","WAVES","LRC"]
    temp = combinations(listesymboles, 2)
    newlist=[]
    for j in list(temp):
        #print("j :",j)
        newlist.append(j[0]+j[1])
        newlist.append(j[1]+j[0])
    print(newlist)
    print("len",len(newlist))
    for i in newlist:
        if i not in symboles:
            newlist.remove(i)
    print(newlist)
    print("len",len(newlist))
    start = time.time()

    Makethefile(newlist,symboles)

    end = time.time()
    elapsed = end - start

    print(f'Temps d\'exécution : {elapsed}s')
#endregion
