from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    passwordHash = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)
    #friends = models.ManyToManyField("User", blank=True)
    def __str__(self):
        return self.username

class Friend(models.Model):
    friendedBy = models.CharField(max_length=50)
    friendUserName = models.CharField(max_length=50)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myfriends')
    def __str__(self):
        return self.friendUserName


class Event(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myEvents')
    name = models.CharField(max_length=50)
    type= models.CharField(max_length=50)
    day = models.CharField(max_length=50, unique=True)
    start_time = models.CharField(max_length=25)
    end_time= models.CharField(max_length=50)
    notes = models.CharField(max_length=300)

    def __str__(self):
        return self.event_id


 

