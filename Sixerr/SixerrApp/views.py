from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import *
from .models import *
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.db.models import Q

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
        skills = Skill.objects.all()
    
        skill_search = self.request.GET.get('skill_search', '').strip()
        if skill_search:
            skills = skills.filter(skill_name__icontains=skill_search)
            context['skills'] = skills.order_by('-popularity')
        else:
            context['skills'] = skills.order_by('-popularity')[:10]

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
        if not skill_name:
            context['no_results_message'] = "No mentors available."
            context['mentors'] = User.objects.filter(role='mentor').order_by('-popularity')[:10]
            return context

        try:
            skill = Skill.objects.get(skill_name=skill_name)
        except Skill.DoesNotExist:
            context['no_results_message'] = "No mentors available."
            context['mentors'] = User.objects.filter(role='mentor').order_by('-popularity')[:10]
            return context

        context['skill'] = skill

        # Get all mentors for the selected skill
        mentors = User.objects.filter(skill__skill_name=skill_name, role='mentor')

        # Filter by mentor name IF provided
        mentor_search = self.request.GET.get('mentor_search', '').strip()
        if mentor_search:
            mentors = mentors.filter(first_name__icontains=mentor_search) | mentors.filter(last_name__icontains=mentor_search)

        # Filtering 
        popularity = self.request.GET.get('popularity', None)
        popularity_operator = self.request.GET.get('popularity_operator', 'gt')
        rating = self.request.GET.get('rating', None)
        rating_operator = self.request.GET.get('rating_operator', 'gt')
        hourly_rate = self.request.GET.get('hourly_rate', None)
        hourly_rate_operator = self.request.GET.get('hourly_rate_operator', 'lt')

        if popularity:
            mentors = mentors.filter(popularity__gt=popularity) if popularity_operator == 'gt' else mentors.filter(popularity__lt=popularity)
        if rating:
            mentors = mentors.filter(rating__gt=rating) if rating_operator == 'gt' else mentors.filter(rating__lt=rating)
        if hourly_rate:
            mentors = mentors.filter(hourly_rate__gt=hourly_rate) if hourly_rate_operator == 'gt' else mentors.filter(hourly_rate__lt=hourly_rate)

        # If filtered, show all mentors sorted by popularity
        if any([mentor_search, popularity, rating, hourly_rate]):
            context['mentors'] = mentors.order_by('-popularity')  # Show all mentors
        else:
            context['mentors'] = mentors.order_by('-popularity')[:10]  # Show only top 10 if no filters

        if not context['mentors']:
            context['no_results_message'] = "There are no mentors with that criteria."

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
    
class MentorProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'mentor_profile.html'

    login_url = reverse_lazy('login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['mentor'] = User.objects.get(username=username)
        return context
    
class BookingView(LoginRequiredMixin, TemplateView):
    template_name = 'booking.html'

    login_url = reverse_lazy('login_view')

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        username = self.kwargs.get('username')
        mentor = User.objects.get(username=username)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.mentor = mentor
            booking.booking_id = str(booking.client.username) + str(booking.mentor.username) + str(Booking.objects.count())
            booking.price = mentor.hourly_rate * (booking.end_time - booking.start_time)
            booking.save()
            return redirect('home')
        
        context = self.get_context_data(form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['mentor'] = User.objects.get(username=username)
        context['user'] = self.request.user
        context['booking'] = Booking.objects.filter(mentor=context['mentor'])
        context['form'] = BookingForm() or kwargs.get('form')
        return context
    
class EditBioView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditBioForm
    template_name = 'edit_bio.html'
    login_url = reverse_lazy('login_view')
    
    def get_object(self, queryset=None):
        user = User.objects.get(username=self.kwargs['username'])
        if user != self.request.user:
            raise PermissionDenied
        return user
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})
    
class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'schedule.html'

    login_url = reverse_lazy('login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = Booking.objects.filter(Q(client=self.request.user) | Q(mentor=self.request.user)).order_by('date', 'start_time')

        for booking in bookings:
            booking.start_time = f"{(booking.start_time % 12) + 1}:00 {'AM' if booking.start_time < 12 else 'PM'}"
            booking.end_time = f"{(booking.end_time % 12) + 1}:00 {'AM' if booking.end_time < 12 else 'PM'}"

        context['bookings'] = bookings
        return context