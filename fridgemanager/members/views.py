from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, UpdateUserForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from fridge.models import Product, Fridge, Recipe


def login_user(request):
    if request.method == "POST":  # when the form is submitted
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "There was an error logging in! Try again!"
            messages.success(request, error_message)
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You Were Logged Out!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html', {
        'form': form,
    })


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'update_profile/change_password.html', {
        'form': form
    })


def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user_dashboard')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'update_profile/update_profile.html', {'user_form': user_form})


def user_dashboard(request):
    product_count = Product.objects.all().count()
    fridge_count = Fridge.objects.all().count()
    recipe_count = Recipe.objects.all().count()

    context = {'product_count': product_count, 'fridge_count': fridge_count, 'recipe_count': recipe_count}
    return render(request, 'dashboard.html', context)
