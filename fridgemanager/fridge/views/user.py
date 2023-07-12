from django.core.paginator import Paginator
from django.shortcuts import render

from ..models import Product, Fridge, Recipe


def user_dashboard(request):

    product_count = Product.objects.all().count()
    fridge_count = Fridge.objects.all().count()
    recipe_count = Recipe.objects.all().count()

    context = {'product_count': product_count,
               'fridge_count': fridge_count,
               'recipe_count': recipe_count}
    return render(request, 'user/dashboard.html', context)

