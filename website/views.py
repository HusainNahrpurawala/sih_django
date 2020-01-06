from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Person
from django.http import HttpResponse

# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, 'website/home.html')

    def post(self, request):
        un = request.POST["username"]
        pw = request.POST["password"]

        u = authenticate(username = un, password = pw)
        if u is not None:
            login(request, u)
            p = Person.objects.get(user = u)
            if p.isSecurity:
                return render(request, 'website/security.html')
            else:
                return render(request, 'website/employee.html')
        else:
            return HttpResponse('Fail')