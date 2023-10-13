from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request) :

    return render(request, 'base/home.html')

def loginPage(request) :
    context = {}
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
    user = authenticate(request, username = username, password = password)
    if user is not None :
        login(request, user)
        return redirect('home')
    
    

    return render(request, 'base/login_register.html', context)