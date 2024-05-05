import requests

class KrakenDownloader:
    def __init__(self, tickers) -> None:
        self.tickers = tickers

    def price(self, ticker) -> float:
        pair = ticker.upper() + 'EUR'
        j = requests.get('https://api.kraken.com/0/public/Ticker?pair='+pair).json()
        return float(j['result'][pair]['a'][0])
    
    def ohlc(self, ticker, interval, since) -> dict:
        pair = ticker.upper() + 'EUR'
        rawData = requests.get('https://api.kraken.com/0/public/OHLC?pair='+pair+"&interval="+str(interval)+"&since="+str(since)).json()
        listedData = list(rawData["result"][pair])
        data = {}
        for el in listedData:
            data[el[0]] = {"open": el[1], "close": el[4], "volume": el[6]}
        return data
    
    def contains(self, ticker) -> bool:
        return ticker.upper() in self.tickers