from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.Home.as_view(), name = 'Home'),
    #path('allLogs/', views.allLogs.as_view(), name = 'AllLogs'),
    #path('userLog/', views.UserLog.as_view(), name = 'UserLog'),
    path('signup/', views.SignUp.as_view(), name = 'SignUp'),
    path('Guest/', views.GuestView.as_view(), name = 'Guest'),
    path('logout/', views.Logout, name = 'Logout'),
    
]