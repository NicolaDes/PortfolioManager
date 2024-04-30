from django import forms
from .models import Portfolio, Asset

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'invested', 'assets']

class AssetInPortfolioForm(forms.Form):
    quantity = forms.DecimalField(max_digits=10, decimal_places=5, label='Quantity')
    invested = forms.DecimalField(max_digits=10, decimal_places=5, label='Invested')