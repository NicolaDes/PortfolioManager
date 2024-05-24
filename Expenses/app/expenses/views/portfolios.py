import json
from datetime import datetime
import pandas as pd
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum, F, Case, When, Value
from django.db.models.functions import TruncMonth

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
    nTransactions = portfolio.transaction_set.all().count()

    context = {
        "portfolio": portfolio,
        "nTransactions": nTransactions,
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

def expensesByCategory(transactions):
    txts = transactions.annotate(total_value=Case(When(category__archetype='Expense', then=F('value') - F('percToExclude') * F('value')),default=F('value'))).values('category__classification').annotate(total_sum=Sum('total_value'))
    return [{"name": str(item['category__classification']), "y": abs(float(item['total_sum']))} for item in txts]

def analytics(request, pk, year):
    portfolio = Portfolio.objects.get(pk=pk)

    # Expenses by category
    expensesByCategory = [
        {
            "name": str(item['category__classification']), 
            "y": abs(float(item['total_sum']))} 
            for item in Transaction.objects.filter(portfolio=portfolio, date__year=year, category__archetype='Outcome')
                .annotate(total_value=Case(When(category__archetype='Outcome', then=F('value') - F('percToExclude') * F('value')),default=F('value')))
                .values('category__classification')
                .annotate(total_sum=Sum('total_value'))
        ]


    # Expenses by label
    expensesByLabel = [
        {
            "name": str(item['label']), 
            "y": abs(float(item['total_sum']))} 
            for item in Transaction.objects.filter(portfolio=portfolio, date__year=year, category__archetype='Outcome')
                .annotate(total_value=Case(When(category__archetype='Outcome', then=F('value') - F('percToExclude') * F('value')),default=F('value')))
                .values('label')
                .annotate(total_sum=Sum('total_value'))
        ]

    # Monlty expsenses by category
    expensesMonthlyByCategory = []
    
    for c in Category.objects.all().exclude(archetype='Income'):

        montlyData = []
        for month in range(1, 13):
            res = Transaction.objects.filter(portfolio=portfolio, category=c, date__year=year, date__month=month).annotate(total_value=Case(When(category__archetype='Outcome', then=F('value') - F('percToExclude') * F('value')),default=F('value'))).values('category__classification').annotate(total_sum=Sum('total_value'))
            sumValue = 0
            if res:
                sumValue = float(res[0]['total_sum'])
            montlyData.append(sumValue)
        
        if not all(value == 0 for value in montlyData):
            expensesMonthlyByCategory.append({
                "name": str(c.classification),
                "data": montlyData 
            })

    # Montly expenses by label
    expensesMonthlyByLabel = []
    
    for el in portfolio.transaction_set.filter(date__year=year).values('label').distinct():
        l = el['label']
        montlyData = []
        for month in range(1, 13):
            res = Transaction.objects.filter(portfolio=portfolio, label=l, date__year=year, date__month=month, category__archetype='Outcome').annotate(total_value=Case(When(category__archetype='Outcome', then=F('value') - F('percToExclude') * F('value')),default=F('value'))).values('label').annotate(total_sum=Sum('total_value'))
            sumValue = 0
            if res:
                sumValue = float(res[0]['total_sum'])
            montlyData.append(sumValue)

        if not all(value == 0 for value in montlyData):
            expensesMonthlyByLabel.append({
                "name": str(l),
                "data": montlyData 
            })

    # Cashflow
    totalMontlyByCategory = []
    
    for c in Category.objects.all().exclude(group='Excluded'):

        montlyData = []
        for month in range(1, 13):
            res = Transaction.objects.filter(portfolio=portfolio, category=c, date__year=year, date__month=month).annotate(total_value=F('value') - F('percToExclude') * F('value')).values('category__classification').annotate(total_sum=Sum('total_value'))
            sumValue = 0
            if res:
                sumValue = float(res[0]['total_sum'])
            montlyData.append(sumValue)
        
        if not all(value == 0 for value in montlyData):
            totalMontlyByCategory.append({
                "name": str(c.classification),
                "data": montlyData 
            })

    cashFlow = []
    cumulativeCashFlow = []
    for month in range(1, 13):
        sumValue = Transaction.objects.filter(portfolio=portfolio, date__year=year, date__month=month).exclude(category__group='Excluded').exclude(category__group='Investments').annotate(total_value=F('value') - F('percToExclude') * F('value')).aggregate(total_sum=Sum('total_value'))['total_sum']

        if sumValue is not None:
            cashFlow.append(float(sumValue))
        else:
            cashFlow.append(float(0))
    
        if len(cumulativeCashFlow) > 0:
            cumulativeCashFlow.append(cumulativeCashFlow[-1] + cashFlow[-1])
        else:
            cumulativeCashFlow.append(cashFlow[-1])

    context = {
        "portfolio": portfolio,
        "expensesByCategory": expensesByCategory,
        "expensesByLabel": expensesByLabel,
        "montlyExpensesByCategory": expensesMonthlyByCategory,
        "montlyExpensesByLabel": expensesMonthlyByLabel,
        "allByCategory": totalMontlyByCategory,
        "cashFlowByMonth": cashFlow,
        "cumulativeCashFlowByMonth": cumulativeCashFlow
    }

    return render(request, "portfolio_analytics.html", context)

def report(request, pk, year, month):
    portfolio = Portfolio.objects.get(pk=pk)
    transactions = []

    for t in portfolio.transaction_set.filter(date__year=year, date__month=month, category__archetype='Outcome').exclude(percToExclude=0):
        transactions.append({
            "id": int(t.pk),
            "description": str(t.description),
            "value": float(t.value),
            "percToExclude": float(t.percToExclude)
        })

    print(transactions)

    context = {
        "portfolio": portfolio,
        "transactions": transactions
    }

    return render(request, "portfolio_report.html", context)