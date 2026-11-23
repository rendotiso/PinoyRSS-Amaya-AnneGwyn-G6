from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
    
    # ER Diagram fields
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.USER)
    display_name = models.CharField(max_length=150, blank=True)
    
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username