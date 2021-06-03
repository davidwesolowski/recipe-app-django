from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from main.models import Roles


def register(response):
    if response.user.is_authenticated:
        return redirect('/')
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']
            user.set_password(form.cleaned_data['password'])
            user.rola = Roles.USER
            user.save()
        else:
            return render(response, 'register/register.html', {'form': form})
        return redirect('/login')
    else:
        form = RegisterForm()
    return render(response, 'register/register.html', {'form': form})


def login_view(response):
    if response.user.is_authenticated:
        return redirect('/')
    if response.method == 'POST':
        form = LoginForm(response.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(response, username=email, password=password)
            if user is not None:
                login(response, user)
                return redirect('/')
            else:
                response.session['invalid_user'] = 1
        else:
            return render(response, 'registration/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(response, 'registration/login.html', {'form': form})


@login_required
def logout_view(response):
    logout(response)
    return redirect('/login')
