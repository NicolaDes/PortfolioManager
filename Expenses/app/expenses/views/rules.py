import re
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from expenses.models import Rule, Category

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

def index(request):
    rules = Rule.objects.all()

    context = {
        "rules": rules
    }

    return render(request, "rule_index.html", context)

@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    name = request.POST.get('name')
    label = request.POST.get('label')
    percentage = request.POST.get('percentage')
    categoryPk = request.POST.get('categoryPk')
    
    category = Category.objects.get(pk=categoryPk)
    rule = Rule(name=name, label=label, percentage=percentage, category=category)

    T = request.POST.get('newRuleType')

    if T == 'regexpr':
        rule.regexpr = request.POST.get('regexpr')
    elif T == 'interval':
        rule.startDate = request.POST.get('startDate')
        rule.endDate = request.POST.get('endDate')

    rule.save()

    return redirect("rule_index")


@csrf_exempt
@require_http_methods(["POST"])
def edit(request):
    pk = request.POST.get('editRuleId')
    name = request.POST.get('editName')
    label = request.POST.get('editLabel')
    percentage = request.POST.get('editPercentage')
    categoryPk = request.POST.get('editCategoryPk')
    
    category = Category.objects.get(pk=categoryPk)
    rule = Rule.objects.get(pk=pk)

    rule.name = name
    rule.label = label
    rule.percentage = percentage
    rule.category = category
    rule.regexpr = None
    rule.startDate = None
    rule.endDate = None

    T = request.POST.get('editRuleType')
    print(f"Type: {T}")
    if T == 'regexpr':
        rule.regexpr = request.POST.get('regexpr')
    elif T == 'interval':
        print(f"Interval dates: {request.POST.get('startDate')} - {request.POST.get('endDate')}")
        rule.startDate = request.POST.get('startDate')
        rule.endDate = request.POST.get('endDate')

    rule.save()

    return redirect("rule_index")

@csrf_exempt
@require_http_methods(["POST"])
def delete(request, pk):
    rule = Rule.objects.get(pk=pk)

    rule.delete()

    return redirect("rule_index")