from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Person
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

class Home(View):

    template_name = 'website/home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        un = request.POST["username"]
        pw = request.POST["password"]

        u = authenticate(username = un, password = pw)
        if u is not None:
            login(request, u)
            p = Person.objects.filter(user = u).first()
            if p.designation == 1: # 1: Employee, 2: Security, 3: Admin
                return render(request, 'website/employee.html')
            elif p.designation == 2:
                return render(request, 'website/security.html')
            elif p.designation == 3:
                return render(request, 'website/admin.html')
        else:
            return HttpResponse('Fail')

class Security(View):

    template_name = 'website/security.html'

    def get(self, request):
        u = request.user
        if u.is_authenticated:
            p = Person.objects.get(user = u)
            g = Guest()
            #if p.isSecurity:
            return render(request, self.template_name)
            #else:
            return HttpResponse('Fail')
        else:
            return redirect(reverse('home'))

class SignUp(View):
    
    template_name = 'website/signup.html'

    def get(self, request):
        #if request.user.is_authenticated:
           # return HttpResponseRedirect(reverse('Security'))
        #else:
        return render(request, self.template_name)

    def post(self, request):
        try:
            p = Person.objects.filter(user = u).first()
            #p = Person()
            user = User()
            user.username = request.POST['username']
            user.set_password(request.POST['password'])
            user.first_name = request.POST['name']
            user.save()
            p.user = user
            p.designation = request.POST['designation']

            if(p.designation == 3):
                p.create_myuser()
            p.save()

        except IntegrityError:
            err = {'error', 'Username already exists!'}
            return render(request, self.template_name, err)

        return HttpResponseRedirect(reverse('Home'))

def Logout(request):
    logout(request)
    return redirect(reverse('home'))