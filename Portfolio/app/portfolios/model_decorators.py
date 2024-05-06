from portfolios.models import Portfolio, Asset, AssetInPortfolio

import requests
import pandas as pd
import json

class AssetView:
    def __init__(self, asset:Asset):
        self.model = asset

        packet = requests.get('http://marketer:8000/'+self.model.ticker).json()

        if packet['alpha'] is not None:
            self._alpha = float(packet['alpha'])
        else:
            self._alpha = None
        
        if packet['beta'] is not None:
            self._beta = float(packet['beta'])
        else:
            self._beta = None
            
        if packet['eur'] is not None:
            self._price = float(packet['eur'])
        else:
            self._price = None

    def download(self):
        packet = requests.get('http://marketer:8000/'+self.model.ticker).json()
        self._alpha = float(packet['alpha'])
        self._beta = float(packet['beta'])
        self._price = float(packet['eur'])

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta(self):
       return self._beta

    @property
    def price(self):
        return self._price

class AssetInPortfolioView:
    def __init__(self, assetInPortfolio:AssetInPortfolio, portfolioValue):
        self.model = assetInPortfolio
        self.currAv = AssetView(self.model.asset)
        self.portfolioValue = portfolioValue
        
    @property
    def alpha(self):
        if self.currAv.alpha is None:
            return None
        return self.currAv.alpha * self.percentage / 100.0
    
    @property
    def beta(self):
        if self.currAv.beta is None:
            return None
        return self.currAv.beta * self.percentage / 100.0

    @property
    def value(self):
        return self.currAv.price * float(self.model.quantity)
    
    @property
    def percentage(self):
        percentageOfPortfolio = (float(self.model.quantity) * self.currAv.price) / self.portfolioValue
        return round((percentageOfPortfolio*100), 2)
        
    @property
    def drawdown(self):
        if self.model.invested <= 0:
            return 0
        return round((((self.value / float(self.model.invested)) - 1.0) * 100), 2)

class PortfolioView:
    def __init__(self, portfolio:Portfolio):
        self.model = portfolio
        self.assets = []
        portfolioValue = self.downloadPortfolioValue()

        for aip in self.model.assetinportfolio_set.all():
            self.assets.append(AssetInPortfolioView(aip, portfolioValue))
        self.assets.sort(key=lambda x: x.drawdown, reverse=True)

    def downloadPortfolioValue(self):
        totalValue = float(self.model.liquidity)
        for a in self.model.assetinportfolio_set.all():
            av = AssetView(a.asset)
            totalValue += float(a.quantity) * av.price
        return totalValue
    
    @property
    def alpha(self):
        weightedAlpha = 0
        for a in self.assets:
            if a.alpha is not None:
                weightedAlpha += a.alpha
        return weightedAlpha
    
    @property
    def beta(self):
        weightedBeta = 0
        for a in self.assets:
            if a.beta is not None:
                weightedBeta += a.beta
        return weightedBeta

    @property
    def value(self):
        totalValue = float(self.model.liquidity)
        for a in self.assets:
            totalValue += a.value
        return totalValue
    
    @property
    def drawdown(self):
        return round(((self.value / float(self.model.invested)) - 1.0) * 100, 2)