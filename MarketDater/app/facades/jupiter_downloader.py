import requests

class JupiterDownloader:
    def __init__(self, tickers) -> None:
        self.tickers = tickers

    def price(self, ticker) -> float:
        upperTicker = ticker.upper()
        url = "https://price.jup.ag/v4/price?ids="+upperTicker
        headers = {"accept": "application/json"}
        j = requests.get(url=url, headers=headers).json()
        price = float(j['data'][upperTicker]['price'])
        againstSymbol = str(j['data'][upperTicker]['vsTokenSymbol'])

        exchangePair = againstSymbol.upper() + 'EUR'
        j = requests.get('https://api.kraken.com/0/public/Ticker?pair=' + exchangePair).json()
        exchangePairValue = float(j['result'][exchangePair]['a'][0])
        
        return price * exchangePairValue
    
    def ohlc(self, ticker, interval, since) -> dict:
       return {}
    
    def contains(self, ticker) -> bool:
        return ticker.upper() in self.tickers