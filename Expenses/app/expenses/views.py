import re
from datetime import datetime
import pandas as pd
from django.shortcuts import render
from django.utils import timezone

from expenses.models import *
from .forms import ExcelUploadForm

# Create your views here.
def home(request):
    portfolios = Portfolio.objects.all()

    context = {
        "portfolios": portfolios
    }

    return render(request, "home.html", context)

def applyRule(transaction, rule):
    if transaction.label is not None or transaction.category is not None:
        return
    if rule.txId is not None:
        if rule.txId.pk == transaction.pk:
            transaction.percToExclude = rule.percentage
            transaction.label = rule.label
            transaction.category = rule.category

            transaction.save()
    elif rule.startDate is not None and rule.endDate is not None:
        if transaction.date >= rule.startDate and transaction.date <= rule.endDate:
            print(f"Applying date rule for {transaction.description}")
            transaction.percToExclude = rule.percentage
            transaction.label = rule.label
            transaction.category = rule.category
            
            transaction.save()
    elif rule.regexpr is not None:
        found = False
        for s in rule.regexpr.split(','):
            pattern = r"(?i)\b" + s + r"\b"
            if re.findall(pattern, transaction.description):
                found = True
                break
        if found:
            transaction.percToExclude = rule.percentage
            transaction.label = rule.label
            transaction.category = rule.category
            
            transaction.save()

def applyRules(portfolio):
    for t in portfolio.transaction_set.all():
        for rip in portfolio.ruleinportfolio_set.all():
            applyRule(t, rip.rule)

def portfolio_detail(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)

    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Esegui l'analisi del file Excel qui
            excel_file = form.cleaned_data['excel_file']
            df = pd.read_excel(excel_file)
            
            starting_row = int(request.POST.get('startingRow', 20))
            date_column = int(request.POST.get('dateColumn', 0))
            description_column = int(request.POST.get('descriptionColumn', 2))
            value_column = int(request.POST.get('valueColumn', 7))

            extracted_data = df.iloc[starting_row - 1:]
            for index, row in extracted_data.iterrows():
                newTx = Transaction(value=row.iloc[value_column], description=row.iloc[description_column], date=timezone.make_aware(row.iloc[date_column], timezone.get_current_timezone()), portfolio=portfolio)
                newTx.save()
            
            applyRules(portfolio=portfolio)
    else:
        form = ExcelUploadForm()


    context = {
        "portfolio": portfolio,
        "form": form
    }

    return render(request, "portfolio_detail.html", context)