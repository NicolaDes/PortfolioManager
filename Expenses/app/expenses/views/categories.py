import re
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from expenses.models import Category


def index(request):
    categories = Category.objects.all()

    context = {
        "categories": categories
    }

    return render(request, "category_index.html", context)

@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    archetype = request.POST.get('archetype')
    classification = request.POST.get('classification')
    group = request.POST.get('group')

    category = Category(archetype=archetype, classification=classification, group=group)

    category.save()

    return redirect("category_index")


@csrf_exempt
@require_http_methods(["POST"])
def edit(request):
    pk = request.POST.get('categoryId')
    archetype = request.POST.get('archetype')
    classification = request.POST.get('classification')
    group = request.POST.get('group')

    category = Category.objects.get(pk=pk)

    category.archetype = archetype
    category.classification = classification
    category.group = group

    category.save()

    return redirect("category_index")

@csrf_exempt
@require_http_methods(["POST"])
def delete(request, pk):
    category = Category.objects.get(pk=pk)

    category.delete()

    return redirect("category_index")