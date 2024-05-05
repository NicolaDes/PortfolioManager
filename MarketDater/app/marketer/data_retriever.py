from app.facades.downloader.ticker_downloader_facade import TickerDownloaderFacade

class DataRetriever:
    def __init__(self, redis):
        self.redis = redis
        self.downloader = TickerDownloaderFacade()
        self.downloadAll()
    
    def downloadAll(self):
        tickers = self.redis.lrange("tickers", 0, -1)

        for t in tickers:
            ticker = t.decode('utf-8')
            print(f"Downloading {ticker}...")

            # Price
            price = self.downloader.price(ticker)
            self.redis.set(ticker, price)

    def download(self, ticker):
        price = self.downloader.price(ticker)
        if price is not None:
            self.redis.set(ticker, price)

    def ohlc(self, ticker, interval, since):
        return self.downloader.ohlc(ticker, interval=interval, since=since)