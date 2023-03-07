from django.db import models
from authentication.models import User

# Create your models here.

class Skill(models.Model):
    name=models.CharField(max_length=100)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)

