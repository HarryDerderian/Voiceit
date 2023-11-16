from django.shortcuts import render, redirect
from django.urls import path
from  users.models import User
from django.contrib.auth import authenticate, login, logout
from . forms import PetitionForm
from django.contrib.auth.decorators import login_required
from . models import Petition, Category, PetitionReply, Signature
from users.forms import SignUpForm
from django.contrib import messages
from . import emailer

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
                # Send an email to the user confirming the creation of the petition.
                emailer.petition_created_email(new_petition.author.username, 
                                               new_petition.author.email, new_petition.title)
                return redirect('/petition/'+ str(new_petition.id))
    return render(request, 'base/create-petition.html', context)

def petitions(request) :
    # A list of all petition objects, and categories
    context = {"petitions" : Petition.objects.all(),
                "categories" : Category.objects.all() }    
    # Triggers if user selects a category from dropdown menu
    if request.method == "POST" :
        # Fetch the id of the category
        requested_category_id = request.POST.get('q')
        try : # Will fail if "all" is selected, its not a category... Hence try-catch
            requested_category = Category.objects.get(id = requested_category_id)
            requested_petitions = Petition.objects.filter(category = requested_category)
            context = {"petitions" : requested_petitions,
                "categories" : Category.objects.all() }
        except : # if any unforseen requests are made, just return all petitions to be displayed
             context = {"petitions" : Petition.objects.all(),
                "categories" : Category.objects.all() } 
    return render(request, 'base/petitions.html', context)

def petition(request, pk) :
    # Check if the request method is GET
    if request.method == "GET" :
        # Confirm requested petition exists
        if Petition.objects.filter(id = pk).exists() :
            # Retrieve the requested petition
            requested_petition = Petition.objects.get(id = pk)
            # Retrieve all signatures associated with the petition
            petition_signatures = Signature.objects.filter(petition = requested_petition)
            # Retrieve all users who have a signatures, on the petition
            users = []
            for signature in petition_signatures :
                users.append(signature.owner)    
            # Retrieve all replies associated with the petition
            replies = PetitionReply.objects.filter(petition = requested_petition)
            # Prepare context with the requested petition and its replies/signatures
            context = {'petition' : requested_petition, 
                                        'replies' : replies, 
                                                'signatures' : petition_signatures,
                                                                            'users' : users}
            # Render the petition.html template with the prepared context
            return render(request, 'base/petition.html', context)
        else :
            # Redirect to the 'petitions' page if the requested petition does not exist
            return redirect('petitions')
    # Check if the request method is POST
    elif request.method == "POST" :
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the form triggering POST: signature, or reply.
            form_type = request.POST.get('form_type')
            # Check if the form type is for submitting a reply
            if form_type ==  "submit_reply":
                # Get user, comment, and the current petition
                user =  request.user
                comment = request.POST.get('reply')
                current_petition = Petition.objects.get(id = pk)
                # Create a new reply and save it
                reply = PetitionReply(author = user, description = comment, petition = current_petition)
                reply.save()
                # Redirect to the petition page after submitting the reply
                return redirect('/petition/'+str(pk))
            # Check if the form type is for signing a petition
            elif form_type == "sign_petition" :
                # Get user and the petition to be signed
                if create_signature(request.user, Petition.objects.get(id = pk)) :
                    messages.success(request, "You have successfully signed the petition!")
                return redirect('/petition/'+str(pk))
        # Redirect to the login page if the user is not authenticated
        else :
            redirect_path = '/petition/'+str(pk)
            return redirect("/login/?previous=" + redirect_path)

def create_signature(user, petition_obj) -> bool:
    # Firstly, its important to check that the user has not already signed the petition
    if Signature.objects.filter(owner = user, petition = petition_obj).exists() :
        return False
    else :
    # Create a new signature and save it
        signature = Signature(owner = user, petition = petition_obj)
        signature.save()
    # We must also update the signature count of the petition.
    petition_obj.total_signatures += 1
    # Now we check to see if the petition has reached its signature goal
    if petition_obj.total_signatures == petition_obj.signature_goal :
         # Retrieve all signatures associated with the petition
            petition_signatures = Signature.objects.filter(petition = petition_obj)
            # Retrieve all users who have a signatures, on the petition
            user_emails = []
            for signature in petition_signatures :
                user_emails.append(signature.owner.email)
            # Mail all users who signed the petiton, alerting them the petition reached its signature goal
            emailer.goal_reached_email(user_emails, petition_obj)
    petition_obj.save()
    return True



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
         #messages.error(request, "unauthorized access")         
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
        else :
            messages.error(request, "Invalid Username/Password")
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
                # Send an email to the user welcoming them to the website.
                emailer.welcome_email(user.username, user.email)
            return redirect('home')
    context = {'form' : form}
    return render(request, 'base/register.html', context)

@login_required(login_url = "/login/?previous=/create-petition/")
def profile(request, pk) :
    # Confirm the user is only able to access their own profile page
    user = request.user
    if not int(user.id) == int(pk) :
        return redirect('home')
    else :
        users_petitions = Petition.objects.filter(author = user)
        user_comments = PetitionReply.objects.filter(author = user)
        user_signatures = Signature.objects.filter(owner = user)
        context = {
            "user" : user,
            "users_petitions" : users_petitions,
            "user_comments" : user_comments,
            "user_signatures" : user_signatures,
        }
        return render(request, 'base/profile.html', context)


