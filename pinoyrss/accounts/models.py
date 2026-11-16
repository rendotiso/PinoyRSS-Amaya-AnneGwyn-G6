from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )

    preferred_regions = models.JSONField(default=list, blank=True)  
    preferred_languages = models.JSONField(default=list, blank=True) 

    def __str__(self):
        return self.username