import json
from datetime import datetime
import pandas as pd
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.http import JsonResponse

from expenses.models import Portfolio, Transaction, Rule, RuleInPortfolio, Category

from .rules import applyRules
from ..forms import ExcelUploadForm

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


    toBeDecidedCategory = Category.objects.filter(classification="ToBeDecided").first()
    nUncategorized = Transaction.objects.filter(portfolio=portfolio, category__isnull=True).count()
    nToBeDecided = Transaction.objects.filter(portfolio=portfolio, category=toBeDecidedCategory).count()
    categories = Category.objects.all()

    context = {
        "portfolio": portfolio,
        "nUncategorized": nUncategorized,
        "nToBeDecided": nToBeDecided,
        "categories": categories,
        "form": form
    }

    return render(request, "portfolio_detail.html", context)

def portfolio_rules(request, pk):
    portfolio = Portfolio.objects.get(pk=pk)
    
    rips = set(rule_in_portfolio.rule for rule_in_portfolio in portfolio.ruleinportfolio_set.all())
    rules = set(Rule.objects.all())

    notRips = rules - rips

    context = {
        "portfolio": portfolio,
        "rips": rips,
        "notRips": notRips 
    }

    return render(request, "portfolio_rules.html", context)

@csrf_exempt
@require_http_methods(["POST"])
def portfolio_assign_rules(request):

    rawData = json.loads(request.body)
    portfolioPk = rawData['portfolioPk']
    rules = rawData['assignedRules']
    
    portfolio = Portfolio.objects.get(pk=portfolioPk)
    
    portfolio.ruleinportfolio_set.all().delete()

    assignedRules = []

    for r in rules:
        rule = Rule.objects.get(pk=r)
        rip = RuleInPortfolio(rule=rule, portfolio=portfolio)
        rip.save()

        assignedRules.append(rip.pk)
    
    return JsonResponse({'message': f'Regole assegnate: {assignedRules}'})