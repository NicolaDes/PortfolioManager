from django.db import models


class Asset(models.Model):
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return f"Ticker: {self.ticker}"

class Portfolio(models.Model):
    name = models.CharField(max_length=100)
    invested = models.DecimalField(max_digits=20, decimal_places=10)
    liquidity = models.DecimalField(max_digits=20, decimal_places=10)
    assets = models.ManyToManyField(Asset, through='AssetInPortfolio')

    def __str__(self):
        return f"Name: {self.name} | Invested: {self.invested}"

class AssetInPortfolio(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    portfolio= models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    invested = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return f"{self.asset} in {self.portfolio}"