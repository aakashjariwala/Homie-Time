from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    passwordHash = models.CharField(max_length=50)

    def __str__(self):
        return "%s"%(self.username)

    class Meta:
        db_table="Test"


