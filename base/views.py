from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from . models import Petition, Category

def petitions(request) :
    # A list of all petition objects, and categories
    context = {"petitions" : Petition.objects.all(),
               "categories" : Category.objects.all() }
    return render(request, 'base/petitions.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request) :
    return render(request, 'base/home.html')

def aboutUs(request):
    return render(request, 'base/about.html')


def registerPage(request) :
    form = UserCreationForm()
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('login')

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