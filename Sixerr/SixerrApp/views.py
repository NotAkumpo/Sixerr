from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def register_view(request):
    msg = None
    skills = Skill.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('login_view')
        else:
            username = form.data['username']
            password = form.data['password1']
            msg = 'An error has occured.'
            if User.objects.filter(username=username).exists():
                msg = 'An account already exists with this username.' 
            try: 
                validate_password(password)
            except forms.ValidationError as e:
                msg = e
    else:
        form = RegistrationForm()
    
    return render(request,'register.html', {'form': form, 'msg': msg, 'skills': skills})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.role == 'client':
                login(request, user)
                return redirect('home')
            elif user is not None and user.role == 'mentor':
                login(request, user)
                return redirect('mentor_home')
            elif User.objects.filter(username=username).exists():
                msg = 'Invalid password.'
            else:
                msg = 'Account with this username does not exist.'

        else:
            msg = 'An error has occured.'
    return render(request,'login.html', {'form': form, 'msg': msg})

def logout_view(request):
    logout(request)
    return redirect('login_view')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    login_url = reverse_lazy('login_view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'client':
            return redirect('mentor_home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()  
        return context

def skill_add_view(request):
    if request.method == 'POST':
        form = SkillForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = SkillForm()
    return render(request, 'skill_add.html', {'form': form})

class MentorListView(LoginRequiredMixin, TemplateView):
    template_name = 'mentor_list.html'

    login_url = reverse_lazy('login_view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'client':
            return redirect('mentor_home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_name = self.kwargs.get('skill_name')
        context['skill'] = Skill.objects.get(skill_name=skill_name)
        context['mentors'] = User.objects.filter(skill__skill_name=skill_name, role='mentor')
        return context


class MentorHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'mentor_home.html'

    login_url = reverse_lazy('login_view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'mentor':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    login_url = reverse_lazy('login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['user'] = User.objects.get(username=username)
        return context