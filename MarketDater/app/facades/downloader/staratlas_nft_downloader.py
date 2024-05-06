import requests

class StaratlasNft:
    def __init__(self, tickers) -> None:
        self.tickers = tickers

    def price(self, ticker) -> float:
        if ticker.upper() == 'PF4':
            return 470.0
        return 0.0
    
    def ohlc(self, ticker, interval, since) -> dict:
      return {}
    
    def contains(self, ticker) -> bool:
        return ticker.upper() in self.tickers