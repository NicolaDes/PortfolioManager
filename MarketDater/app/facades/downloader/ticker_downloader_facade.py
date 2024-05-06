from app.facades.downloader.kraken_downloader import KrakenDownloader
from app.facades.downloader.magiceden_downloader import MagicedenDownloader
from app.facades.downloader.staratlas_nft_downloader import StaratlasNft
from app.facades.downloader.jupiter_downloader import JupiterDownloader

import json

class TickerDownloaderFacade:
    def __init__(self) -> None:
        tickersPath = 'app/data/tickers.json'
        with open(tickersPath, 'r') as file:
            tickers = json.load(file)

        self.krakenDownloader = KrakenDownloader(tickers=tickers['kraken'])
        self.magicedenDownloader = MagicedenDownloader(tickers=tickers['magiceden'])
        self.staratlasNftDownloader = StaratlasNft(tickers=tickers['staratlas_nft'])
        self.jupiterDownloader = JupiterDownloader(tickers=tickers['jupiter'])

    def price(self, ticker):
        if self.krakenDownloader.contains(ticker):
            return self.krakenDownloader.price(ticker)
        elif self.magicedenDownloader.contains(ticker):
            return self.magicedenDownloader.price(ticker)
        elif self.staratlasNftDownloader.contains(ticker):
            return self.staratlasNftDownloader.price(ticker)
        elif self.jupiterDownloader.contains(ticker):
            return self.jupiterDownloader.price(ticker)
        else:
            return None
        
    def ohlc(self, ticker, interval, since):
        if self.krakenDownloader.contains(ticker):
            return self.krakenDownloader.ohlc(ticker=ticker, interval=interval, since=since)
        else:
            return None