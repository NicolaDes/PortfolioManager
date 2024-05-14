import re
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from expenses.models import Transaction, Portfolio, Category

@csrf_exempt
@require_http_methods(["POST"])
def edit(request):
    pk = request.POST.get('transactionId')
    portfolioPk = request.POST.get('portfolioId')
    categoryPk = request.POST.get('categoryPk')
    value = request.POST.get('value')
    description = request.POST.get('description')
    date = request.POST.get('date')
    percentage = request.POST.get('percentage')
    label = request.POST.get('label')

    transaction = Transaction.objects.get(pk=pk)
    portfolio = Portfolio.objects.get(pk=portfolioPk)
    category = Category.objects.get(pk=categoryPk)

    transaction.value = value
    transaction.description = description
    transaction.date = date
    transaction.percentageToExclude = percentage
    transaction.label = label
    transaction.portfolio = portfolio
    transaction.category = category

    transaction.save()

    return redirect("portfolio_detail", portfolioPk)

@csrf_exempt
@require_http_methods(["POST"])
def delete(request, pk):
    transaction = Transaction.objects.get(pk=pk)

    portfolioPk = transaction.portfolio.pk

    transaction.delete()

    return redirect("portfolio_detail", portfolioPk)