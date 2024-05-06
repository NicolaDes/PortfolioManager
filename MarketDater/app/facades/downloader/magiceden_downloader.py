import requests

class MagicedenDownloader:
    def __init__(self, tickers) -> None:
        self.tickers = tickers

    # Return price in EUR
    def price(self, ticker) -> float:
        j = requests.get('https://api.kraken.com/0/public/Ticker?pair=SOLEUR').json()
        solPrice = float(j['result']["SOLEUR"]['a'][0])

        url = "https://api-mainnet.magiceden.dev/v2/collections/"+ticker+"/stats"
        headers = {"accept": "application/json"}
        j = requests.get(url=url, headers=headers).json()
        # avgPrice = (float(j['avgPrice24hr']) / 1000000000.0) * solPrice # Warning: not all tickers has avgPrice24Hr
        floorPrice = (float(j['floorPrice']) / 1000000000.0) * solPrice
        
        return floorPrice
    
    def ohlc(self, ticker, interval, since) -> dict:
       return {}
    
    def contains(self, ticker) -> bool:
        return ticker in self.tickers