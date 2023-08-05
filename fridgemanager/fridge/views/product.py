from django.shortcuts import render, redirect
from ..models import Product, Fridge
from ..forms import ProductForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


def product_list(request):
    fridges_of_user = Fridge.objects.filter(owners=request.user)

    # Retrieve products from all fridges of the user
    products_of_user = Product.objects.filter(fridge__in=fridges_of_user).order_by('created_date')

    p = Paginator(products_of_user, 2)  # 2nd arg --> objects per page
    page = request.GET.get('page')
    products_to_show = p.get_page(page)

    return render(request, 'product/product_list.html',
                  {'products': products_to_show, 'products_len': len(products_of_user)})


def product_add(request):
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/products/add?submitted=True')
    else:
        form = ProductForm()
        form.fields['fridge'].queryset = Fridge.objects.filter(owners=request.user)
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'product/product_add.html',
                  {'form': form, 'submitted': submitted})


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product/product_details.html', {'product': product})


def product_update(request, product_id):
    product = Product.objects.get(pk=product_id)
    form = ProductForm(request.POST or None, instance=product)
    form.fields['fridge'].queryset = Fridge.objects.filter(owners=request.user)

    if form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'product/product_update.html', {'product': product, 'form': form})


def product_delete(request, product_id):
    product = Product.objects.get(pk=product_id)
    fridge = product.fridge
    for owner in fridge.owners.all():
        if request.user == owner:
            product.delete()
            messages.success(request, 'Product deleted!')
            return redirect('product_list')

    messages.error(request, 'You are unauthorized to delete this product!')
    return redirect('product_list')


def products_search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        # products = Product.objects.filter(name__contains=searched)  # single field of model
        products = Product.objects.filter(
            Q(name__contains=searched) |
            Q(description__contains=searched) |
            Q(amount__contains=searched) |
            Q(amount_unit__contains=searched)
        )
        return render(request, 'product/product_search.html',
                      {'searched': searched, 'products': products})
    else:
        return render(request, 'product/product_search.html', {})




