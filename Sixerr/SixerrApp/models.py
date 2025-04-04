from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Skill(models.Model):
    skill_name = models.CharField(
        primary_key=True,
        unique=True,
        null=False, 
        max_length=20
        )
    
    image = models.ImageField(upload_to='images/skills/', null=False, blank=False, default='images/skills/default.jpg')

    popularity = models.IntegerField(default=0)
    
    def __str__(self):
           return self.skill_name

class User(AbstractUser):
    class Role(models.TextChoices):
        MENTOR = 'mentor'
        CLIENT = 'client'

    default_role = Role.CLIENT

    image = models.ImageField(upload_to='images/users/', null=False, blank=False, default='images/users/default.jpg')

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=default_role
    )

    first_name = models.CharField(null=False, max_length=255, default='John')
    last_name = models.CharField(null=False, max_length=255, default='Smith')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    dummy = models.BooleanField(default=False)
    popularity = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    hourly_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    join_date = models.DateField(auto_now_add=True, null=False, blank=False)
    bio = models.TextField(null=False, blank=False, default='I love Sixerr!')

class Booking(models.Model):
    booking_id = models.CharField(
        primary_key=True,
        unique=True,
        null=False, 
        max_length=20
        )
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='client_bookings')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='mentor_bookings')

    date = models.DateField(null=False, blank=False)
    start_time = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(23)])
    end_time = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(23)])
    price = models.FloatField(null=False, blank=False, default=0.0, validators=[MinValueValidator(0.0)])
    modality = models.CharField(null=False, blank=False, max_length=20, default='onsite')
