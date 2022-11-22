from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def editEvent(request):
    return render(request, 'editEvent.html')

def createEvent(request):
    return render(request, 'createEvent.html')
    
def home(request):
    return render(request, 'home.html')

def viewcal(request):
    return render(request, 'viewcal.html')
