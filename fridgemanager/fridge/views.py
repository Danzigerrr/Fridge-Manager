from django.shortcuts import render
from .models import Product


def home(request):
    return render(request, 'fridge/home.html', {})


def all_products(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'fridge/products_list.html', {'products': products})
