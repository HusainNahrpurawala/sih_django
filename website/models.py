from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    designation = models.IntegerField(choices=((1,"Employee"), (2,"Security"), (3,"Admin")), default=1)

    def __str__(self):
        return str(self.user.username)