import re
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from expenses.models import Budget

@csrf_exempt
@require_http_methods(["POST"])
def delete(request, pk):
    budget = Budget.objects.get(pk=pk)
    portfolioPk = budget.portfolio.pk

    budget.delete()

    return redirect("portfolio_budgets", portfolioPk)