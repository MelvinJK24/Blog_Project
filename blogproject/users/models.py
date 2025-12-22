from django.db import models
from django.contrib.auth.models import User
from constants import genders, roles

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=genders)
    role = models.CharField(max_length=7, choices=roles)
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username