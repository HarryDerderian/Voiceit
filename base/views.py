from django.shortcuts import render, redirect
from django.urls import path
from  users.models import User
from django.contrib.auth import authenticate, login, logout
from . forms import PetitionForm
from django.contrib.auth.decorators import login_required
from . models import Petition, Category, PetitionReply
from users.forms import SignUpForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# this neat little trick requires usesr to be signed in to view this page.
@login_required(login_url = "/login/?previous=/create-petition/")
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
                email_subject = "Your Voicelt Petition Has Been Created"
                # I KNOW ITS UGLY BUT IDK HOW TO FORMAT IT WITHOUT IT LOOKING OUT OF PLACE
                # IF YOU CAN FIND A WAY BE MY GUESS
                email_message = f"""Dear {new_petition.author.username},

Congratulations on creating your petition: {new_petition.title}, on Voicelt! You've taken the first step toward making a positive change on your campus.

Now, it's time to gather signatures and build support for your cause. Share your petition with fellow students, friends, and colleagues to help it gain momentum. When you reach your signature goal, we'll notify you with a special message of achievement.

Thank you for being an active member of the Voicelt community and for your dedication to making a local impact. Your voice matters, and together, we can create meaningful change on campus.

Best of luck with your petition, and keep up the great work!

Sincerely,
The Voicelt Team"""
                send_mail(
                            email_subject,
                            email_message,
                            settings.EMAIL_HOST_USER,
                            [new_petition.author.email],
                            fail_silently=False,
                        )
                return redirect('/petition/'+ str(new_petition.id))
    return render(request, 'base/create-petition.html', context)

def petitions(request) :
    # A list of all petition objects, and categories
    context = {"petitions" : Petition.objects.all(),
               "categories" : Category.objects.all() }
    return render(request, 'base/petitions.html', context)

def petition(request, pk) :
    if request.method == "GET" :
        if Petition.objects.filter(id = pk).exists() :
            requested_petition = Petition.objects.get(id = pk)
            context = {'petition': requested_petition,
            'replies' : PetitionReply.objects.filter(petition = requested_petition) }
            return render(request, 'base/petition.html', context)
        else :
            return redirect('petitions')
    elif request.method == "POST" :
        if request.user.is_authenticated:
            user =  request.user
            comment = request.POST.get('reply')
            current_petition = Petition.objects.get(id = pk)
            reply = PetitionReply(author = user, description = comment, petition = current_petition)
            reply.save()
            return redirect('/petition/'+str(pk))
        else :
            redirect_path = '/petition/'+str(pk)
            return redirect("/login/?previous=" + redirect_path)

# SIGN/UNSIGN
# GET USER, GET PETITON, UPDATE PETITION SIGNATURE COUNT
# CREATE/REMOVE SIGNATURE OBJECT



@login_required(login_url = "/login/")
def edit_petition(request, pk) :
    """Edits a petition, user must be logged in, 
    and the creator of the petition. If the user is not logged in
    or not the petition owner redirect them"""
    # Confirm petition exists :
    if not Petition.objects.filter(id = pk).exists() :
         return redirect('petitions')
    requested_petition = Petition.objects.get(id = pk)
    user = request.user
    # Confirm the current user is the author of the petition
    if not user == requested_petition.author:
         messages.error(request, "unauthorized access")         
         return redirect('petitions')
    else :
        update_form =  PetitionForm(instance=requested_petition)
        if request.method == "POST":
        # Bind the form to the POST data
            update_form = PetitionForm(request.POST, instance = requested_petition)
        if update_form.is_valid():
            # Save the form to update the petition object
            update_form.save()
            return redirect('/petition/'+str(pk))
        context = {"form" : update_form ,"petition" : requested_petition}
        return render(request, 'base/edit-petition.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request) :
    return render(request, 'base/home.html')

def aboutUs(request):
    return render(request, 'base/about.html')

def loginPage(request, redirect_path = 'home') :
    context = {}
    redirect_path = request.GET.get('previous', 'home')
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None :
            login(request, user)
            return redirect(redirect_path)
    return render(request, 'base/login.html', context)

def registerPage(request) :
    form = SignUpForm()
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid() :
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username = user.username, email=user.email, password=raw_password) 
            if user is not None :
                login(request, user)
                email_subject = "Welcome to Voicelt - Empower Your Campus Voice"
                # I KNOW ITS UGLY BUT IDK HOW TO FORMAT IT WITHOUT IT LOOKING OUT OF PLACE
                # IF YOU CAN FIND A WAY BE MY GUESS
                email_message = f"""Dear {user.username},

Welcome to Voicelt, your platform for creating change on campus. With Voicelt, you can:

- Create petitions for campus issues.
- Collect signatures from like-minded students.
- Make a local impact.

Join us in bringing positive change to your college. Start now!

Sincerely,
The Voicelt Team
"""
                send_mail(
                            email_subject,
                            email_message,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False,
                        )
            return redirect('home')
    context = {'form' : form}
    return render(request, 'base/register.html', context)