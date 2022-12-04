from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import *
from django.http import *
from .forms import *


def index(request):
    return render(request, 'index.html')

def login(request):

    valid = True
    #get user object from database
    if request.method == 'POST':
        username = request.POST.get('username')
        user_obj = None
        try:
            user_obj = User.objects.get(username=username)
            valid = True 
        except:
            valid = False
            return HttpResponse("Error, in log in! Check if username and password\nis correct or if you have an account with us :)")
        if valid:
            if user_obj.passwordHash == request.POST.get('PasswordHash'):
                request.session["username"] = username
                #request.session["firstname"] = user_obj.firstname
                #request.session["lastname"] = user_obj.lastname
                #request.session["email"] = user_obj.email
                #request.session["bio"] = user_obj.bio
                return HttpResponseRedirect("../home")     
            else:
                return HttpResponse("Error, in log in! Check if username and password\nis correct or if you have an account with us :)")
    return render(request, 'login.html')

def profile(request):

    username = request.session["username"]
    user = User.objects.get(username=username)

    context = {}
    context["firstname"] = user.firstname
    context["lastname"] = user.lastname
    context["email"] = user.email
    context["username"] = user.username
    context["bio"] = user.bio

    return render(request, 'profile.html', context)

def createAccount(request):

    #Add User object into database
    """
    context = {}
    #user = User.objects.create()
    if "username" in request.GET:
        username = request.GET["username"]
        print(username)
        if (User.objects.filter(username=username)).exists():
            context["exists"] = True
            return redirect('../createAccount/', context)
        else:
            context["exists"] = False
            return render(request, 'createAccount.html', context)
    """

        
    if request.method == "POST":
        username = request.POST.get("username")
        #print(username)    
        if User.objects.filter(username=username).exists():
            return HttpResponse("Sorry, A user with this username already exists, try again!")
        if request.POST.get("password") == request.POST.get("password-re"):
            user = User.objects.create()
            user.passwordHash = request.POST.get("password")
            user.firstname = request.POST.get("firstname")
            user.lastname = request.POST.get("lastname")
            user.email = request.POST.get("email")
            user.bio = request.POST.get("bio")
            user.username = username
            user.save()
        else:
            return HttpResponse("Password does not match, try again!")
        return HttpResponseRedirect("..")
    return render(request, 'createAccount.html')


def editEvent(request):
    return render(request, 'editEvent.html')

def createEvent(request):
    return render(request, 'createEvent.html')
    
def home(request):
    return render(request, 'home.html')

def viewcal(request):
    return render(request, 'viewcal.html')

def homielist(request):
    return render(request, 'homielist.html')

def findtime(request):
    return render(request, 'findtime.html')

def test_post(request):
    return render(request, 'login.html')

