import json
from decimal import Decimal
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .forms import PortfolioForm, AssetInPortfolioForm
from .model_decorators import AssetView, PortfolioView
from portfolios.models import Portfolio, Asset, AssetInPortfolio

# Create your views here.
def portfolio_index(request):
    portfolios = Portfolio.objects.all()
    context = {
        "portfolios": portfolios
    }

    return render(request, "portfolios/portfolio_index.html", context)

def portfolio_detail(request, pk):
    portfolio = PortfolioView(Portfolio.objects.get(pk=pk))
    context = {
        "portfolio": portfolio
    }

    return render(request, "portfolios/portfolio_detail.html", context)

def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            form.save()
            # Post save actions here
    else:
        form = PortfolioForm()
        
    return render(request, 'portfolio_form.html', {'form': form})

@csrf_exempt
@require_http_methods(["POST"])
def get_ticker_infos(request, pk):
    data = json.loads(request.body)
    ticker = data['ticker']
    quantity = float(data['quantity'])

    asset, created = Asset.objects.get_or_create(ticker=ticker)
    portfolio = Portfolio.objects.get(pk=pk)

    aView = AssetView(asset=asset)
    pView = PortfolioView(portfolio=portfolio)

    price = aView.price
    alpha = aView.alpha
    beta = aView.beta
    value = price * quantity

    portfolioAlpha = ((pView.value * pView.alpha) + (value * alpha)) / (pView.value + value)
    portfolioBeta = ((pView.value * pView.beta) + (value * beta)) / (pView.value + value)

    print(f"(({pView.value} * {pView.alpha}) + ({value} * {alpha}) / ({pView.value} + {value})")
    print(f"(({pView.value} * {pView.beta}) + ({value} * {beta}) / ({pView.value} + {value})")
    
    values = {
        'price': price,
        'alpha': alpha,
        'beta': beta,
        'portfolioAlpha': portfolioAlpha,
        'portfolioBeta': portfolioBeta
    }

    return JsonResponse(values)

@csrf_exempt
@require_http_methods(["POST"])
def add_ticker(request, pk):
    ticker = request.POST.get('ticker')
    quantity = Decimal(request.POST.get('quantity'))
    invested = Decimal(request.POST.get('invested'))

    asset, __created = Asset.objects.get_or_create(ticker=ticker)
    portfolio = Portfolio.objects.get(pk=pk)
    assetInPortfolio, created = AssetInPortfolio.objects.get_or_create(asset=asset, portfolio=portfolio, invested=invested, quantity=quantity)

    if not created:
        assetInPortfolio.invested += invested
        assetInPortfolio.quantity += quantity
        assetInPortfolio.save()

    portfolio.liquidity -= invested
        
    portfolio.save()

    context = {
        "portfolio": PortfolioView(portfolio)
    }

    return redirect("portfolio_detail", pk=pk)


@csrf_exempt
@require_http_methods(["POST"])
def remove_ticker(request, pk):
    data = json.loads(request.body)
    ticker = data['ticker']
    quantity = float(data['quantity'])
    invested = float(data['invested'])

    asset, __created = Asset.objects.get_or_create(ticker=ticker)
    portfolio = Portfolio.objects.get(pk=pk)
    assetInPortfolio, created = AssetInPortfolio.objects.get_or_create(asset=asset, portfolio=portfolio)

    if created:
        portfolio.assets.add(assetInPortfolio)
    else:
        assetInPortfolio.invested += invested
        assetInPortfolio.quantity += quantity
        assetInPortfolio.save()
        
    portfolio.save()

    context = {
        "portfolio": portfolio
    }

    return render(request, "portfolios/portfolio_detail.html", context)
