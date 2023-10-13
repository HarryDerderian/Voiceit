from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def logout_view(request):
    logout(request)
    redirect('home')

def home(request) :
    return render(request, 'base/home.html')


def registerPage(request) :
    form = UserCreationForm()
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/register.html', context)

def loginPage(request) :
    context = {}
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None :
            login(request, user)
            return redirect('home')
    return render(request, 'base/login.html', context)