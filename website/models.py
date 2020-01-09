from django.db import models
from django.contrib.auth.models import User
from .__init__ import path

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    designation = models.IntegerField(choices=((1,"Employee"), (2,"Security"), (3,"Admin")), default=1)
    photo = models.ImageField(default=path + 'photos/default.jpg')
    isPresent = models.BooleanField(default = "True")

    def __str__(self):
        return str(self.user.username)


class Guest(models.Model):
    name = models.CharField(max_length=100, default='N/A')
    photo = models.ImageField(default=path + 'photos/default.jpg')

    def __str__(self):
        return self.name