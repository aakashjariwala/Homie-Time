from django.shortcuts import render, redirect
from urllib3 import Retry
from Test.models import User
from Test.forms import UserForm

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def registration(request):
    return render(request, 'registration.html')

def userfunc(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("/show")
            except:
                pass
    else:
        form = UserForm()
    #keep temptable.html consistent with show
    return render(request, 'index.html', {'form':form})


def show(request):
    user = User.objects.all()
    #define show.html in your files
    return render(request, 'show.html', {'user': user}) 

def edit(request,id):
    user = User.objects.get(id=id)
    return render(request, 'edit.html', {'user': user})

def update(request, id):
    user = user.objects.get(id=id)
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        #show is here
        return redirect("/show")
    return render(request, 'edit.html', {'user':user})

def destroy(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/show")








