from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Person, Guest
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
import os
from .__init__ import path
from .CreateEnc import encode
import csv
from .TodayLogs import TodayLogs
import pandas as pd
from django.urls import reverse
from django.contrib import messages


class Home(View):

    template_name = 'website/home.html'

    def get(self, request):
        if request.user.is_authenticated: 
            p = Person.objects.get(user = request.user)
            if p.designation == 1: # 1: Employee, 2: Security, 3: Admin
                csvfile = pd.read_csv(path+'website/Logs/'+str(p.user.pk)+'.csv')
                csvfile = csvfile.drop(columns=['Unnamed: 0'])
                csvHtml = csvfile.to_html()
                return render(request, 'website/employee.html', {'p':p,'csv':csvHtml})
            elif p.designation == 2:
                return render(request, 'website/security.html')
            elif p.designation == 3:
                return render(request, 'website/admin.html')
        return render(request, self.template_name)

    def post(self, request):
        un = request.POST["username"]
        pw = request.POST["password"]

        u = authenticate(username = un, password = pw)
        if u is not None:
            login(request, u)
            p = Person.objects.filter(user = u).first()
            if p.designation == 1: # 1: Employee, 2: Security, 3: Admin
                csvfile = pd.read_csv(path+'website/Logs/'+str(p.user.pk)+'.csv')
                csvfile = csvfile.drop(columns=['Unnamed: 0'])
                csvHtml = csvfile.to_html()
                return render(request, 'website/employee.html', {'p':p,'csv':csvHtml})
            elif p.designation == 2:
                return render(request, 'website/security.html')
            elif p.designation == 3:
                return render(request, 'website/admin.html')
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return render(request, 'website/home.html')

class SignUp(View):
    
    template_name = 'website/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else: return render(request, "website/home.html")

    def post(self, request):
        try:
            p = Person()
            user = User()
            user.username = request.POST['username']
            user.set_password(request.POST['password'])
            user.first_name = request.POST['name']
            user.save()
            p.user = user
            p.designation = request.POST['designation']
            p.photo = request.FILES['photo']
            ext = p.photo.name.split('.')[-1]
            p.photo.name = str(user.pk) + '.' + ext
            if int(p.designation) == 3:
                user.is_staff = True
                user.is_admin = True
                user.is_superuser = True
                user.save()
            p.save()
            encode(str(user.pk), False)

        except IntegrityError:
            err = {'error', 'Username already exists!'}
            return render(request, self.template_name, err)

        return render(request, 'website/admin.html')

class GuestView(View):
    template_name = 'website/guest.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else: return render(request, "website/home.html")

    def post(self, request):
        g = Guest()
        g.name = request.POST['name']
        g.save()
        g.photo = request.FILES['photo']
        ext = ext = g.photo.name.split('.')[-1]
        g.photo.name = 'g' + str(g.pk) + '.' + ext
        g.save()
        encode(str(g.pk), True)
        return render(request, 'website/security.html')

class allLogs(View):
    template_name = 'website/allLogs.html'

    def get(self,request):
        if request.user.is_authenticated:
            TodayLogs()
            csvfile = pd.read_csv(path+'website/Today.csv')
            csvfile = csvfile.drop(columns=['Unnamed: 0'])
            csvHtml = csvfile.to_html()
            print(csvfile)
            return render(request, 'website/allLogs.html', {'csv': csvHtml})
        else:
            return render(request, "website/home.html")

def Logout(request):
    logout(request)
    return redirect('website:Home')