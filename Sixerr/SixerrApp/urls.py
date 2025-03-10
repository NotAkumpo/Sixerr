from SixerrApp import views
from django.urls import path

from .views import *

urlpatterns = [
    path('login', views.login_view, name='login_view'),
    path('register', views.register_view, name='register_view'),
    path('home', views.home, name='home'),
    path('logout', views.logout_view, name='logout_view'),
    path('skills', views.skill_view, name='skill_view'),
]