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
    
    #Add Event object into database
    username = request.session['username']
    user = User.objects.get(username=username)
    if request.method == "POST":
            name = request.POST.get("name")
            start_time = request.POST.get("start_time")
            if Event.objects.filter(name=name, start_time=start_time).exists():
                return HttpResponse("Sorry event like this already exists!")
            event = Event.objects.create(user=user)
            event.name = name
            event.start_time = start_time
            event.type = request.POST.get("type")
            event.day = request.POST.get("day")
            event.end_time = request.POST.get("end_time")
            event.notes = request.POST.get("notes")
            event.save()
            return HttpResponseRedirect("../home/")
    return render(request, 'createEvent.html')
    
def home(request):

    return render(request, 'home.html')

def viewcal(request):
    context = {}


    return render(request, 'viewcal.html', context)
    context = {}
    context["name"] = "Birthday"
    context["type"] = "Party"
    context["day"] = "Monday December 12"
    context["start_time"] = "7 pm"
    context["end_time"] = "7 pm"
    context["notes"] = "yuhhhhhhhhhhhhhhh"
    # return render(request, 'viewcal.html')
    return render(request, 'viewcal.html', context)


def seeFriendList(username):
    try:
        return User.objects.get(username=username).myfriends.all()
    except:
        return False

def seeEventsList(username):
    try:
        return User.objects.get(username=username).myEvents.all()
    except:
        return False

def getFriend(friendUserName):

    friend_obj = None
    try:
        friend_obj = User.objects.get(username=friendUserName)
        return friend_obj
    except:
        return False


def homielist(request):

    context = {}
    username = request.session["username"]
    print("Logged in as: " + username)
    user_obj = User.objects.get(username=username)
    if request.method == "POST":
        desired_friend = request.POST.get('friend')
        friend_obj = None
        try:
            friend_obj = User.objects.get(username=desired_friend)
        except:
            return HttpResponse("Sorry this user does not exist, you got played fool")
        if Friend.objects.filter(friendedBy=username, friendUserName=desired_friend, friend=friend_obj).exists():
            return HttpResponse("You're already friends")
        else:
            new_friend = Friend.objects.create(friendedBy=username, friendUserName=desired_friend, friend=user_obj)
            new_friend.save()
            print(new_friend.friendedBy, new_friend.friendUserName, User.objects.get(username=username).myfriends.all())
            return HttpResponseRedirect("../homielist/")
    
    #Example of how you can access friend information
    myfriend = seeFriendList(username=username)
    context['friends'] = myfriend
    #print(myfriend)
    #myfriendInfo = getFriend(friendUserName=myfriend[0])
    #print(myfriendInfo.bio)
    
    return render(request, 'homielist.html', context)

def findtime(request):

    context = {}
    username = request.session['username']
    user = User.objects.get(username=username)
    events = seeEventsList(username)
    #event = Event.objects.filter(event_id=).values('id')
    #print(event)

    #Right now I am getting all items but I need to filter these
    #items based on user id
    events = seeEventsList(user)
    print(events)

    return render(request, 'findtime.html', context)

def test_post(request):
    return render(request, 'login.html')

