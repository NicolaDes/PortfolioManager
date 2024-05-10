from django.db import models

# Create your models here.
class Portfolio(models.Model):
    name = models.CharField(max_length=20)

class Category(models.Model):
    archetype = models.CharField(max_length=20)
    classification = models.CharField(max_length=20)
    group = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.archetype} | {self.classification} | {self.group}"
    
class Transaction(models.Model):
    value = models.DecimalField(max_digits=20, decimal_places=3)
    description = models.CharField(max_length=100)
    date = models.DateTimeField()
    percToExclude = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    label = models.CharField(max_length=20, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

class Rule(models.Model):
    name = models.CharField(max_length=20)
    label = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=10, decimal_places=4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    regexpr = models.CharField(max_length=100, null=True)
    startDate = models.DateTimeField(null=True)
    endDate = models.DateTimeField(null=True)
    txId = models.ForeignKey(Transaction, null=True, on_delete=models.CASCADE)

class RuleInPortfolio(models.Model):
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

