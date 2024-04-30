import requests
import datetime as dt
import json

class MarketData:
    def __init__(self, redis) -> None:
        self.redis = redis

    def addSymbol(self, type, symbol):
        upperSymbol = symbol.upper()
        self.redis.rpush(type, upperSymbol)
        j = requests.get('https://api.kraken.com/0/public/Ticker?pair='+upperSymbol).json()
        price = float(j['result'][upperSymbol]['a'][0])
        
        print(f"Adding {upperSymbol} -> {price}")
        
        self.redis.set(upperSymbol, price)

    def isNew(self, symbol) -> bool:
        upperSymbol = symbol.upper()
        if self.redis.exists(upperSymbol):
            return False
        
        try:
            j = requests.get('https://api.kraken.com/0/public/Ticker?pair='+upperSymbol).json()
            price = float(j['result'][upperSymbol]['a'][0])
            if price >= 0.0:
                return True
            return False
        except:
            return False
    
    def price(self, symbol) -> float:
        upperSymbol = symbol.upper()
        return self.redis.get(upperSymbol)
    
    def ohlc(self, symbol, interval=1440, since=dt.datetime(2021, 1, 1).timestamp()):
        upperSymbol = symbol.upper()
        timeOfRequest = int(round(dt.datetime.now().timestamp()))
        if not self.redis.exists("ohcl:" + upperSymbol):
            rawData = requests.get('https://api.kraken.com/0/public/OHLC?pair='+upperSymbol+"&interval="+str(interval)+"&since="+str(since)).json()
            listedData = list(rawData["result"][upperSymbol])
            data = {}
            for el in listedData:
                data[el[0]] = {"open": el[1], "close": el[4], "volume": el[6]}
            self.redis.set("ohcl:" + upperSymbol, json.dumps(data))
            self.redis.set("ohcl:" + upperSymbol + ":timeOfRequest", timeOfRequest)
        else:
            lastTimeOfRequest = int(self.redis.get("ohcl:" + upperSymbol + ":timeOfRequest"))
            print(f"Ticker already present. Last request was done @ {lastTimeOfRequest}")

            if timeOfRequest > lastTimeOfRequest + interval:
                print(f"Retrieving new data...")
                
                rawData = requests.get('https://api.kraken.com/0/public/OHLC?pair='+upperSymbol+"&interval="+str(interval)+"&since="+str(since)).json()
                listedData = list(rawData["result"][upperSymbol])
                data = {}
                for el in listedData:
                    data[el[0]] = {"open": el[1], "close": el[4], "volume": el[6]}
                self.redis.set("ohcl:" + upperSymbol, json.dumps(data))
                self.redis.set("ohcl:" + upperSymbol + ":timeOfRequest", timeOfRequest)
        
        return self.redis.get("ohcl:" + upperSymbol)
        