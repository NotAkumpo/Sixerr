from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Skill(models.Model):
    skill_name = models.CharField(
        primary_key=True,
        unique=True,
        null=False, 
        max_length=20
        )
    
    image = models.ImageField(upload_to='images/', null=False, blank=False, default='images/default.jpg')
    
    def __str__(self):
           return self.skill_name

class User(AbstractUser):
    class Role(models.TextChoices):
        MENTOR = 'mentor'
        CLIENT = 'client'

    default_role = Role.CLIENT

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=default_role
    )

    first_name = models.CharField(null=False, max_length=255, default='John')
    last_name = models.CharField(null=False, max_length=255, default='Smith')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True, related_name='users')

