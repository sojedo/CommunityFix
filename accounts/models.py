from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('resident', 'Resident'),
        ('admin', 'Administrator'),
        ('officer', 'Field Officer'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='resident'
    )