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
from django.core.serializers.json import DjangoJSONEncoder
from string import ascii_lowercase
import json
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404, redirect

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
                return redirect('mentor_profile', username=username) # redirect to mentor profile
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
            return redirect('mentor_profile', username=request.user.username)
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

class SkillsListView(LoginRequiredMixin, TemplateView):
    template_name = 'skillslist.html'

    login_url = reverse_lazy('login_view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'client':
            return redirect('mentor_profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skillslist = Skill.objects.all()

        letters = []
        for s in skillslist:
            if s.skill_name[0] not in letters:
                letters.append(s.skill_name[0])

        context['skillslist'] = skillslist
        context['letters'] = letters

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
            return redirect('mentor_profile', username=request.user.username)
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

        # Sorting by selected field and order
        sort_by = self.request.GET.get('sort_by', 'popularity')  # Default to sorting by popularity
        order = self.request.GET.get('order', 'desc')  # Default to descending order

        if order == 'asc':
            mentors = mentors.order_by(sort_by)  # Ascending order
        else:
            mentors = mentors.order_by('-' + sort_by)  # Descending order

        # Filtering by popularity, rating, and hourly rate
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

        # Handle no mentors
        if mentors.exists():
            context['mentors'] = mentors
        else:
            context['no_results_message'] = "There are no mentors with that criteria."
            context['mentors'] = []

        return context
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    login_url = reverse_lazy('login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['user'] = User.objects.get(username=username, role='client')
        return context
    
class MentorProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'mentor_profile.html'

    login_url = reverse_lazy('login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['mentor'] = User.objects.get(username=username)
        availability = Availability.objects.filter(user=context['mentor']).order_by('start_time')
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        availability = sorted(availability, key=lambda a: day_order.index(a.day))
        for a in availability:
            a.start_time = f"{(a.start_time % 12) if a.start_time not in [0, 12] else 12}:00 {'AM' if a.start_time < 12 else 'PM'}"
            a.end_time = f"{(a.end_time % 12) if a.end_time not in [12, 24] else 12}:00 {'AM' if a.end_time < 12 or a.end_time == 24 else 'PM'}{' ND' if a.end_time == 24 else ''}"
        context['availability'] = availability

        return context
    
class BookingView(LoginRequiredMixin, TemplateView):
    template_name = 'booking.html'

    login_url = reverse_lazy('login_view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'client':
            return redirect('mentor_profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        username = self.kwargs.get('username')
        mentor = User.objects.get(username=username)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.mentor = mentor
            booking.booking_id = str(booking.client.username) + str(booking.mentor.username) + str(Booking.objects.count())
            booking.price = round(mentor.hourly_rate * (booking.end_time - booking.start_time), 2)
            booking.save()
            self.request.user.balance = round(self.request.user.balance - booking.price, 2)
            self.request.user.save()
            mentor.popularity += 1
            mentor.balance = round(mentor.balance + booking.price, 2)
            mentor.save()
            mentor.skill.popularity += 1
            mentor.skill.save()
            return redirect('home')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['mentor'] = User.objects.get(username=username)
        context['user'] = self.request.user
        bookings = Booking.objects.filter(mentor=context['mentor'])
        context['bookings'] = json.dumps(list(bookings.values('date', 'start_time', 'end_time')), cls=DjangoJSONEncoder)
        
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
        if self.request.user.role == 'client':
            return reverse_lazy('profile', kwargs={'username': self.request.user.username})
        else:
            return reverse_lazy('mentor_profile', kwargs={'username': self.request.user.username})

class EditRateView(LoginRequiredMixin, UpdateView):
    form_class = EditRateForm
    template_name = 'edit_rate.html'
    login_url = reverse_lazy('login_view')
    
    def get_object(self, queryset=None):
        user = User.objects.get(username=self.kwargs['username'])
        if user != self.request.user or user.role != 'mentor':
            raise PermissionDenied
        return user
    
    def get_success_url(self):
        return reverse_lazy('mentor_profile', kwargs={'username': self.request.user.username})

class AddBalanceView(LoginRequiredMixin, UpdateView):
    form_class = AddBalanceForm
    template_name = 'add_balance.html'
    login_url = reverse_lazy('login_view')
    
    def get_object(self, queryset=None):
        user = User.objects.get(username=self.kwargs['username'])
        if user != self.request.user or user.role != 'client':
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
            booking.start_time = f"{(booking.start_time % 12) if booking.start_time not in [0, 12] else 12}:00 {'AM' if booking.start_time < 12 else 'PM'}"
            booking.end_time = f"{(booking.end_time % 12) if booking.end_time not in [12, 24] else 12}:00 {'AM' if booking.end_time < 12 or booking.end_time == 24 else 'PM'}{' ND' if booking.end_time == 24 else ''}"

        context['bookings'] = bookings
        return context
    
class AddAvailabilityView(LoginRequiredMixin, TemplateView):
    template_name = 'add_availability.html'

    login_url = reverse_lazy('login_view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'mentor':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user
            availability.save()
            return redirect('mentor_profile', username=request.user.username)
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        availabilities = Availability.objects.filter(user=self.request.user)
        context['availabilities'] = json.dumps(list(availabilities.values('day', 'start_time', 'end_time')), cls=DjangoJSONEncoder)
        context['form'] = AvailabilityForm() or kwargs.get('form')
        return context
    
@login_required
def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id)

    if request.user == availability.user:
        availability.delete()

    return redirect('mentor_profile', username=request.user.username)


# class BookingView(LoginRequiredMixin, TemplateView):
#     template_name = 'booking.html'

#     login_url = reverse_lazy('login_view')

#     def post(self, request, *args, **kwargs):
#         form = BookingForm(request.POST)
#         username = self.kwargs.get('username')
#         mentor = User.objects.get(username=username)

#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.client = request.user
#             booking.mentor = mentor
#             booking.booking_id = str(booking.client.username) + str(booking.mentor.username) + str(Booking.objects.count())
#             booking.price = round(mentor.hourly_rate * (booking.end_time - booking.start_time), 2)
#             booking.save()
#             self.request.user.balance = round(self.request.user.balance - booking.price, 2)
#             self.request.user.save()
#             mentor.popularity += 1
#             mentor.balance = round(mentor.balance + booking.price, 2)
#             mentor.save()
#             mentor.skill.popularity += 1
#             mentor.skill.save()
#             return redirect('home')
        
#         context = self.get_context_data(**kwargs)
#         context['form'] = form
#         return self.render_to_response(context)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         username = self.kwargs.get('username')
#         context['mentor'] = User.objects.get(username=username)
#         context['user'] = self.request.user
#         bookings = Booking.objects.filter(mentor=context['mentor'])
#         context['bookings'] = json.dumps(list(bookings.values('date', 'start_time', 'end_time')), cls=DjangoJSONEncoder)
        
#         context['form'] = BookingForm() or kwargs.get('form')
#         return context