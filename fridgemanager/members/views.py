from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


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
    logout_message = "You were successfully logged out!"
    messages.success(request, logout_message)
    return redirect('home')


def register_user(request):
    if request.method == "POST":  # when the form is submitted
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # the first password (confirmation)
            user = authenticate(username=username, password=password)
            login(request, user)
            success_message = 'Registration successful!'
            messages.success(request, success_message)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register_user.html',
                  {'form': form})
