from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User, Skill, Booking
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all(),
        required=False
    )
    username = forms.CharField()
    password1 = forms.CharField(
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput()
    )
    email = forms.EmailField()
    role = forms.ChoiceField(
        choices=User.Role.choices,
        initial=User.Role.MENTOR
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'skill', 'username', 'password1', 'password2', 'email', 'role', 'image']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'image']

class EditBioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio']

class BookingForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
        input_formats=['%Y-%m-%d'],
    )
    start_time = forms.IntegerField(
        widget=forms.Select(choices=[
            (i, f'{(i % 12) if i not in [0, 12] else 12}:00 {"AM" if i < 12 else "PM"}') for i in range(24)
        ], attrs={'id': 'start-time'}), 
        validators=[MinValueValidator(0), MaxValueValidator(23)],
        required=True
    )
    end_time = forms.IntegerField(
        widget=forms.Select(choices=[
            (i, f'{(i % 12) if i not in [12, 24] else 12}:00 {"AM" if i < 12 or i == 24 else "PM"}{" ND" if i == 24 else ""}') for i in range(1, 25)
        ], attrs={'id': 'end-time'}),   
        validators=[MinValueValidator(1), MaxValueValidator(24)],
        required=True
    )
    modality = forms.ChoiceField(
        choices=[('onsite', 'Onsite'), ('online', 'Online')],
        initial='onsite'
    )

    class Meta:
        model = Booking
        fields = ['date', 'start_time', 'end_time', 'modality']