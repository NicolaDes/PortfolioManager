import datetime as dt
import json

class MarketData:
    def __init__(self, redis, dr) -> None:
        self.redis = redis
        self.dr = dr

    def price(self, ticker) -> float:
        if not self.redis.exists(ticker):
            self.redis.rpush('tickers', ticker)
            self.dr.download(ticker)

        return self.redis.get(ticker)
    
    def ohlc(self, ticker, interval=1440, since=dt.datetime(2021, 1, 1).timestamp()):
        data = self.dr.ohlc(ticker=ticker, interval=interval, since=since)

        return json.dumps(data)
    
    def alpha(self, ticker) -> float:
        return 0.0
    
    def beta(self, ticker) -> float:
        return 0.0