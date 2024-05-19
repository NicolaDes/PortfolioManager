from django.shortcuts import render

from expenses.models import Portfolio

# Create your views here.
def home(request):
    portfolios = Portfolio.objects.all()

    context = {
        "portfolios": portfolios
    }

    return render(request, "home.html", context)