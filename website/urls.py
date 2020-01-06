from django.urls import path
from . import views

app_name = 'site'

urlpatterns = [
    path('', views.Home.as_view(), name = 'Home'),
]