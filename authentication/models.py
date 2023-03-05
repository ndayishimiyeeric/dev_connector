from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email=models.EmailField(unique=True)
    profil_image=models.ImageField(upload_to="photos/profils/",null=True)
    USERNAME_FIELD='username'
    REQUIRED_FIELDS = []

    #def get_username(self):
    #    return self.email
