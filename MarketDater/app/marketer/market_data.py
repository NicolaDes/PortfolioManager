import datetime as dt
import pandas as pd
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
    
    def alpha(self, ticker, interval=1440, since=dt.datetime(2021, 1, 1).timestamp()) -> float:
        if self.redis.exists("alpha:"+ticker):
            return self.redis.get("alpha:"+ticker)

        tickerData = self.dr.ohlc(ticker=ticker, interval=interval, since=since)
        if tickerData is None:
            return None

        #TODO: Check which market index should compare to
        btcData = self.dr.ohlc(ticker='wbtc', interval=interval, since=since)

        btcReturns = pd.Series([float(btcData[k]['close']) for k in btcData]).pct_change() * 100

        tickerReturns = pd.Series([float(tickerData[k]['close']) for k in tickerData]).pct_change() * 100
        beta = (tickerReturns.cov(btcReturns) / btcReturns.var())
        alpha = (tickerReturns.iloc[-1] - (beta * (btcReturns.mean())))

        self.redis.set("alpha:"+ticker, alpha)

        return alpha

    def beta(self, ticker, interval=1440, since=dt.datetime(2021, 1, 1).timestamp()) -> float:
        if self.redis.exists("beta:"+ticker):
            return self.redis.get("beta:"+ticker)
        
        tickerData = self.dr.ohlc(ticker=ticker, interval=interval, since=since)
        if tickerData is None:
            return None

        #TODO: Check which market index should compare to
        btcData = self.dr.ohlc(ticker='wbtc', interval=interval, since=since)

        btcReturns = pd.Series([float(btcData[k]['close']) for k in btcData]).pct_change() * 100

        tickerReturns = pd.Series([float(tickerData[k]['close']) for k in tickerData]).pct_change() * 100
        beta = (tickerReturns.cov(btcReturns) / btcReturns.var())
        self.redis.set("beta:"+ticker, beta)

        return beta