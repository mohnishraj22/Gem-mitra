from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('',views.index),
    path('geturl',views.geturl),
    path('about',views.about,name='about'),
    path('login',views.login,name='login'),
    path('contact',views.contact,name='contact'),
    path('help',views.help,name='help'),
]
