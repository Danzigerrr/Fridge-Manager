from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, UpdateUserForm, UserProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from django.db.models import Count

# Add higher directory to python modules path:
import sys
sys.path.append("..")  
from fridge.models import Product, Fridge, Recipe


def login_user(request):
    if request.method == "POST":  # when the form is submitted
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # update daily points
            today_date = datetime.date.today()
            last_login_date = user.last_login.date()
            if last_login_date != today_date:
                user.userprofile.daily_points = 10
                user.userprofile.save()

            # login user
            login(request, user)

            return redirect('user_dashboard')
        else:
            error_message = "There was an error logging in! Try again!"
            messages.error(request, error_message)
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
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)

            # create a user profile for the user
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            messages.success(request, "Registration Successful!")
            return redirect('home')
    else:
        form = RegisterUserForm()
        profile_form = UserProfileForm()

    return render(request, 'authenticate/register_user.html', {
        'form': form, 'profile_form': profile_form
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
    current_user = request.user
    fridges_of_user = Fridge.objects.filter(owners=current_user)
    fridge_count = fridges_of_user.count()

    product_count = 0
    for fridge in fridges_of_user:
        product_count += Product.objects.filter(fridge=fridge).count()

    recipe_count = Recipe.objects.filter(saved_by=current_user).count()

    context = {'fridge_count': fridge_count, 'product_count': product_count, 'recipe_count': recipe_count}
    return render(request, 'dashboard.html', context)
