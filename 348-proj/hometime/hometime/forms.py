from django import forms
from .models import User


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




