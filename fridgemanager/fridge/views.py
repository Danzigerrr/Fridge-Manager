from django.shortcuts import render, redirect
from .models import Product, Fridge
from .forms import FridgeForm, ProductForm
from django.http import HttpResponseRedirect


def home(request):
    return render(request, 'fridge/home.html', {})


def all_products(request):
    products = Product.objects.all()
    print(products)
    return render(request, 'fridge/products_list.html', {'products': products})


def add_product(request):
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_product?submitted=True')
    else:
        form = ProductForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'fridge/product_add.html',
                  {'form': form, 'submitted': submitted})


def add_fridge(request):
    submitted = False
    if request.method == "POST":
        form = FridgeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_fridge?submitted=True')
    else:
        form = FridgeForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'fridge/fridge_add.html',
                  {'form': form, 'submitted': submitted})


def all_fridges(request):
    fridges = Fridge.objects.all()
    return render(request, 'fridge/fridge_list.html', {'fridges': fridges})


# fridge_id comes from the url
def fridge_detail(request, fridge_id):
    fridge = Fridge.objects.get(pk=fridge_id)
    return render(request, 'fridge/fridge_details.html', {'fridge': fridge})


# fridge_id comes from the url
def fridge_update(request, fridge_id):
    fridge = Fridge.objects.get(pk=fridge_id)
    form = FridgeForm(request.POST or None, instance=fridge)
    if form.is_valid():
        form.save()
        return redirect('all_fridges')

    return render(request, 'fridge/fridge_update.html',
                  {'fridge': fridge,
                   "form": form})

