from django.db import models
#import uuid

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    passwordHash = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)

    def __str__(self):
        return self.username


class people(models.Model):
    dad = models.CharField(max_length=30)
    mom = models.IntegerField()

    def __str__(self):
        return self.dad


