from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User
from .models import Skill

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
        fields = ['first_name', 'last_name', 'skill', 'username', 'password1', 'password2', 'email', 'role']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'image']