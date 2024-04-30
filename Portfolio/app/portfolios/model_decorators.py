from portfolios.models import Portfolio, Asset, AssetInPortfolio

import requests
import pandas as pd
import json

class AssetView:
    def __init__(self, asset:Asset):
        self.model = asset

    @property
    def alpha(self):
        btcStr = requests.get('http://marketer:8000/ohcl/cryptos/WBTCEUR').json()
        btcJson = json.loads(btcStr['ohcl'])
        btc_returns = pd.Series([float(btcJson[k]['close']) for k in btcJson]).pct_change() * 100

        # Download ohcl
        string = requests.get('http://marketer:8000/ohcl/cryptos/'+self.model.ticker+"EUR").json()
        j = json.loads(string['ohcl'])
        
        # Compute returns
        returns = pd.Series([float(j[k]['close']) for k in j]).pct_change() * 100

        # compute alpha
        return (returns.iloc[-1] - (self.beta * (btc_returns.mean())))

    
    @property
    def beta(self):
        # Market index
        btcStr = requests.get('http://marketer:8000/ohcl/cryptos/WBTCEUR').json()
        btcJson = json.loads(btcStr['ohcl'])
        btc_returns = pd.Series([float(btcJson[k]['close']) for k in btcJson]).pct_change() * 100
        
        # Download ohcl
        string = requests.get('http://marketer:8000/ohcl/cryptos/'+self.model.ticker+"EUR").json()
        j = json.loads(string['ohcl'])
        
        # Compute returns
        returns = pd.Series([float(j[k]['close']) for k in j]).pct_change() * 100

        return (returns.cov(btc_returns) / btc_returns.var())

    @property
    def price(self):
        return float(requests.get('http://marketer:8000/cryptos/'+self.model.ticker+"EUR").json()['price'])

class AssetInPortfolioView:
    def __init__(self, assetInPortfolio:AssetInPortfolio):
        self.model = assetInPortfolio
        self.currAv = AssetView(self.model.asset)
        totalValue = float(self.model.portfolio.liquidity)
        for a in self.model.portfolio.assets.all():
            av = AssetView(a)
            totalValue += float(self.model.quantity) * av.price
        self.percentageOfPortfolio = (float(self.model.quantity) * self.currAv.price) / totalValue

    @property
    def alpha(self):
        return self.currAv.alpha * self.percentageOfPortfolio
    
    @property
    def beta(self):
        return self.currAv.beta * self.percentageOfPortfolio

    @property
    def value(self):
        return self.currAv.price * float(self.model.quantity)
    
    @property
    def percentage(self):
        return round((self.percentageOfPortfolio*100), 2)
    
    @property
    def drawdown(self):
        return round(((self.value / float(self.model.invested)) * 100), 2)

class PortfolioView:
    def __init__(self, portfolio:Portfolio):
        self.model = portfolio
        self.assets = []
        for aip in self.model.assetinportfolio_set.all():
            self.assets.append(AssetInPortfolioView(aip))

    @property
    def alpha(self):
        weightedAlpha = 0
        for a in self.assets:
            weightedAlpha += a.alpha
        return weightedAlpha
    
    @property
    def beta(self):
        weightedBeta = 0
        for a in self.assets:
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
        return round((self.value / float(self.model.invested)) * 100, 2)