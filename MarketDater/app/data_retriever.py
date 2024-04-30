import threading
import requests
import time

class DataRetriever(threading.Thread):
    def __init__(self, redis, tout, *args, **kwargs):
        super().__init__(daemon=True, *args, **kwargs)
        self.redis = redis
        self.tout = tout
        self.daemon = True
        self.start()

    def run(self):
        while True:
            self.downloadData()
            time.sleep(self.tout)
    
    def downloadData(self):
        self.downloadCryptos()

    def downloadCryptos(self):
        cryptos = self.redis.lrange("cryptos", 0, -1)
        for c in cryptos:
            symbol = c.decode('utf-8')
            j = requests.get('https://api.kraken.com/0/public/Ticker?pair='+symbol).json()
            price = float(j['result'][symbol]['a'][0])
            self.redis.set(symbol, price)