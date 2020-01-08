from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    designation = models.IntegerField(choices=((1,"Employee"), (2,"Security"), (3,"Admin")), default=1)
    def __str__(self):
        return str(self.user.username)

    def create_myuser(self, *args, **kwargs):
        try:
            super(Person, self).save()  # Call default save method
        except:
            print("Exception occurred:")

class Employee:
    empid = models.IntegerField(default = 0)
    dept = models.CharField(max_length=100)
    isPresent = models.BooleanField("True")

