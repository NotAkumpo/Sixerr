from SixerrApp import views
from django.urls import path
from .views import HomeView

from .views import *

urlpatterns = [
    path('login', views.login_view, name='login_view'),
    path('register', views.register_view, name='register_view'),
    path('home', HomeView.as_view(), name='home'),
    path('logout', views.logout_view, name='logout_view'),
    path('skill_add', views.skill_add_view, name='skill_add_view'),
    path('mentor_list/<str:skill_name>', MentorListView.as_view(), name='mentor_list'),
    path('profile/<username>', ProfileView.as_view(), name='profile'),
    path('mentor_profile/<username>', MentorProfileView.as_view(), name='mentor_profile'),
    path('booking/<username>', BookingView.as_view(), name='booking'),
    path('edit_bio/<username>', EditBioView.as_view(), name='edit_bio'),
    path('schedule', ScheduleView.as_view(), name='schedule'),
    path('skillslist', SkillsListView.as_view(), name='skillslist'),
    path('edit_rate/<username>', EditRateView.as_view(), name='edit_rate'),
    path('add_balance/<username>', AddBalanceView.as_view(), name='add_balance'),
]