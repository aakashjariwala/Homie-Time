from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import *
from django.http import *
from django.db import transaction
from .forms import *
from .database_actions import PreparedStatementHandler

import uuid
import hashlib


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
            temp = hashlib.sha1(request.POST.get('PasswordHash').encode('utf-8')).hexdigest()
            if user_obj.passwordHash == temp:
                request.session["username"] = username
                return HttpResponseRedirect("../home")     
            else:
                return HttpResponse("Error, in log in! Check if username and password\nis correct or if you have an account with us :)")
    return render(request, 'login.html')

def profile(request):

    username = request.session["username"]
    user = User.objects.get(username=username)

    context = {}

    if 'name' in request.GET:
        user.firstname = request.GET['name']
    if 'lastname' in request.GET:
        user.lastname = request.GET['lastname']
    if 'email' in request.GET:
        user.email = request.GET['email']
    if 'bio' in request.GET:
        user.bio = request.GET['bio']
    user.save()

    context["firstname"] = user.firstname
    context["lastname"] = user.lastname
    context["email"] = user.email
    context["username"] = user.username
    context["bio"] = user.bio
    context['custom_image'] = user.profile_pic

    return render(request, 'profile.html', context)

def PreparedStatements(request, rtype, lst):

    username = request.session["username"]
    user = User.objects.get(username=username)
    handler = PreparedStatementHandler(user)

    for i in lst:
        if rtype == i:
            handler.insertDefaultUsers()
        elif rtype == i:
            handler.deletePastEvents()
        else:
            new_handler = PreparedStatementHandler(user)

    return new_handler

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
                user.passwordHash = hashlib.sha1(request.POST.get("password").encode('utf-8')).hexdigest()
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
def deleteEvent(request, event_id):
    try:
        with transaction.atomic():  
            event = Event.objects.get(event_id=uuid.UUID(event_id))
            event.delete()
    except Event.DoesNotExist:
        return HttpResponse("Event has been deleted!")
    return render(request, 'viewcal.html')

    
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
    

def editprofileimage(request):
    context = {}
    username = request.session['username']
    user = User.objects.get(username=username)
    if request.method == "POST":
        #try:
        try:
            form = ProfileEdit(files=request.FILES)
            form.Meta.store_image = request.FILES
            print(request.POST.get("name"))
            user.profile_pic = form.Meta.store_image['image']
            user.save()
            return HttpResponseRedirect("../profile/")
        except:
            return HttpResponse("Something went wrong with upload")
    
    context['custom_image'] = user.profile_pic
    return render(request, 'editprofileimage.html', context)

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

def getfriendObjects(username):
    myfriends = seeFriendList(username)
    friendlist = []
    for friend in myfriends:
        friendlist.append(getFriend(friend))
    return friendlist


def homielist(request):

    context = {}
    username = request.session["username"]
    user_obj = User.objects.get(username=username)
    print("Logged in as: " + username)
    user_obj = User.objects.get(username=username)
    myfriend = seeFriendList(username=username)
    if request.method == "POST":
        if 'friend' in request.POST:
            desired_friend = request.POST.get("friend")
            friend_obj = None
            try:
                friend_obj = User.objects.get(username=desired_friend)
                print(friend_obj)
            except:
                return HttpResponse("Sorry this user does not exist, you got played fool")
            if Friend.objects.filter(friendedBy=username, friendUserName=desired_friend, friend=user_obj).exists():
                print("friend exists")
                return HttpResponse("You're already friends with this person!")
            else:
                print("created friend")
                new_friend = Friend.objects.create(friendedBy=username, friendUserName=desired_friend, friend=user_obj)
                new_friend.save()
                print(new_friend.friendedBy, new_friend.friendUserName, User.objects.get(username=username).myfriends.all())
                return HttpResponseRedirect("../homielist/")
        elif 'viewHomie' in request.POST:
            context2 = {}
            data = request.POST['viewHomie']
            friend = getFriend(data)
            context2['firstname'] = friend.firstname
            context2['lastname'] = friend.lastname
            context2['email'] = friend.email
            context2['bio'] = friend.bio
            context2['username'] = friend.username
            context2['custom_image'] = friend.profile_pic
            return render(request, 'viewHomie.html', context2)
        elif "deleteHomie" in request.POST:
            chosen = request.POST["deleteHomie"]
            test_obj = Friend.objects.filter(friendedBy=username, friendUserName=chosen)
            test_obj.delete()



    myfriend = getfriendObjects(username=username)

    #Example of how you can access friend information
    context['friends'] = myfriend
    context['custom_image'] = user_obj.profile_pic
    
    return render(request, 'homielist.html', context)


def viewHomie(request):
    username = request.session["username"]
    friends = seeFriendList(username=username)
    print(friends)

    return render(request, "viewHomie.html")

def findtime(request):

    context = {}
    username = request.session["username"]
    user_obj = User.objects.get(username=username)
    
    friends = seeFriendList(username)
    context['friends'] = friends
    events = seeEventsList(username)
    context['events'] = events
    
    if request.method == "POST":
        friendUsername = request.POST.get('selectFriend')
        selectedDate = request.POST.get('selectDate')
        context['friendUsername'] = friendUsername
        context['selectedDate'] = selectedDate
        
        if selectedDate == "":
            return HttpResponse("Please select a date!")
    
        if friendUsername == "noSelection":
            return HttpResponse("Please select a friend to schedule Homie Time with!")
        else:
            events =  Event.objects.filter(day=selectedDate)
            friendEvents = seeEventsList(friendUsername)
            context['friendEvents'] = friendEvents
            friend = User.objects.get(username=friendUsername)
            context['firstname'] = friend.firstname
            context['lastname'] = friend.lastname

    return render(request, 'findtime.html', context)

def test_post(request):
    return render(request, 'login.html')