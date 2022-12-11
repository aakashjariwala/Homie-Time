from django import forms
from .models import User, Event


class CreateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = [
        'firstname', 
        'lastname', 
        'username', 
        'passwordHash',
        'email',
        'bio'
        ]


class CreateEvent(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
        'name', 
        'type',
        'day',
        'start_time',
        'end_time',
        'notes'
        ]

class ProfileEdit(forms.ModelForm):
    class Meta:
        model = User
        store_image = forms.ImageField()
        fields = ["firstname", "username", "email", "bio", "profile_pic",]




