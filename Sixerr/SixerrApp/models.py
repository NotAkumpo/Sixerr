from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin'
        CLIENT = 'client'
        MENTOR = 'mentor'

    default_role = Role.CLIENT

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=default_role
    )

    first_name = models.CharField(null=False, max_length=255, default='John')
    last_name = models.CharField(null=False, max_length=255, default='Smith')
    skill = models.CharField(null=True, blank=True, max_length=255)
