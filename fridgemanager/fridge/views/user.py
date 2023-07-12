from ..models import Product, Fridge, Recipe
from django.shortcuts import render


def user_dashboard(request):
    fridges = Fridge.objects.filter(owners=request.user)
    fridge_count = fridges.count()

    # Retrieve products from all fridges of the user
    products = Product.objects.filter(fridge__in=fridges)

    product_count = products.count()

    recipe_count = Recipe.objects.filter(saved_by=request.user).count()

    context = {'product_count': product_count,
               'fridge_count': fridge_count,
               'recipe_count': recipe_count}
    return render(request, 'user/dashboard.html', context)


