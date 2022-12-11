from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import *
from django.http import *
from django.db import transaction
from .forms import *
import uuid


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


    if request.method == "POST":
        #try:
        try:
            form = ProfileEdit(files=request.FILES)
            form.Meta.store_image = request.FILES
            user.profile_pic = form.Meta.store_image['image']
            user.save()
            return HttpResponseRedirect("../profile/")
        except:
            return HttpResponse("Something went wrong with upload")
    context['custom_image'] = user.profile_pic


    return render(request, 'profile.html', context)

@transaction.atomic
def createAccount(request):

    #Add User object into database
    if request.method == "POST":
        username = request.POST.get("username")
        #print(username)    
        if User.objects.filter(username=username).exists():
            return HttpResponse("Sorry, A user with this username already exists, try again!")
        if request.POST.get("password") == request.POST.get("password-re"):
            with transaction.atomic():
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



@transaction.atomic
def editEvent(request, event_id):
    event = Event.objects.get(event_id=uuid.UUID(event_id))
    print("EVENT" + event.name)
    context = {}
    context["name"] = event.name
    context["type"] = event.type
    context["day"] = event.day
    context["start_time"] = event.start_time
    context["end_time"] = event.end_time
    context["notes"] = event.notes

    if request.method == "POST":
            name = request.POST.get("name")
            start_time = request.POST.get("start_time")
            if Event.objects.filter(name=name, start_time=start_time).exists():
                return HttpResponse("Sorry event like this already exists!")
            with transaction.atomic():  
                event = Event.objects.get(event_id=uuid.UUID(event_id))
                event.name = name
                event.start_time = start_time
                event.type = request.POST.get("type")
                event.day = request.POST.get("day")
                event.end_time = request.POST.get("end_time")
                event.notes = request.POST.get("notes")
                event.save()
                return HttpResponseRedirect("../view/")
    return render(request, 'editEvent.html', context)
    
@transaction.atomic
def createEvent(request):
    
    #Add Event object into database
    username = request.session['username']
    user = User.objects.get(username=username)
    if request.method == "POST":
            name = request.POST.get("name")
            start_time = request.POST.get("start_time")
            if Event.objects.filter(name=name, start_time=start_time).exists():
                return HttpResponse("Sorry event like this already exists!")
            with transaction.atomic():  
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

    context = {}
    username = request.session['username']
    user = User.objects.get(username=username)


    context['custom_image'] = user.profile_pic


    return render(request, 'home.html', context)

def viewcal(request):

    context = {}
    username = request.session['username']
    user = User.objects.get(username=username)

    context['custom_image'] = user.profile_pic

    events = seeEventsList(username=username)
    print(events)
    event_list = []
    for event in events:
        val = uuid.UUID(str(event))
        event_list.append(Event.objects.get(event_id=val))
    

    context['events'] = event_list
    if request.method == "POST":
        context2 = {}
        if 'eventButton' in request.POST:
           data = request.POST['eventButton']
           event_obj = getEvent(data)
           context2['event'] = event_obj
           context2['custom_image'] = user.profile_pic
           return render(request, 'editEvent.html', context2)

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

def getEvent(event_id):

    try:
        return Event.objects.get(event_id=uuid.UUID(event_id))
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
    user_obj = User.objects.get(username=username)
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
    context['custom_image'] = user_obj.profile_pic
    #print(myfriend)
    #myfriendInfo = getFriend(friendUserName=myfriend[0])
    #print(myfriendInfo.bio)
    
    return render(request, 'homielist.html', context)

def findtime(request):

    context = {}
    username = request.session["username"]
    user_obj = User.objects.get(username=username)
    context['custom_image'] = user_obj.profile_pic
    
    friends = seeFriendList(username)

    context['friends'] = friends
    events = seeEventsList(username)

    return render(request, 'findtime.html', context)

def test_post(request):
    return render(request, 'login.html')