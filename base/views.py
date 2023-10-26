from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import UserCreationForm
from . forms import PetitionForm
from django.contrib.auth.decorators import login_required
from . models import Petition, Category
from users.forms import SignUpForm

# this neat little trick requires usesr to be signed in to view this page.
@login_required(login_url = "/login/")
def create_petition(request) :
    """
        Brings the user to a page for building petitions.
        Will ask for various input fields relating to a petition object.
        Finally will store the new petition if the inputs are valid.
    """
    input_form = PetitionForm(request.POST)
    context = {"form" : input_form}
    if request.method == "POST" :
        # Checking if input is valid and a user is logged in.
        if input_form.is_valid() :
                new_petition = input_form.save()
                new_petition.author = request.user
                new_petition.save()
                return redirect('petitions')
    return render(request, 'base/create-petition.html', context)

def petitions(request) :
    # A list of all petition objects, and categories
    context = {"petitions" : Petition.objects.all(),
               "categories" : Category.objects.all() }
    return render(request, 'base/petitions.html', context)

def petition(request, pk) :
    if Petition.objects.filter(id = pk).exists() :
        context = {'petition': Petition.objects.get(id = pk)}
        return render(request, 'base/petition.html', context)
    else :
         return redirect('petitions')


def logout_view(request):
    logout(request)
    return redirect('home')

def home(request) :
    return render(request, 'base/home.html')

def aboutUs(request):
    return render(request, 'base/about.html')




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



def registerPage(request) :
    form = SignUpForm()
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid() :
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            login(request, user)
            return redirect('home')
    context = {'form' : form}
    return render(request, 'base/register.html', context)