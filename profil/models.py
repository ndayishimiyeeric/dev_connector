from django.db import models
from authentication.models import User

# Create your models here.

class Profil(models.Model):
    status=models.CharField(max_length=100)
    bio = models.TextField(max_length=300)
    location=models.CharField(max_length=50)
    linkedin_link=models.CharField(max_length=50,null=True)
    github_link=models.CharField(max_length=50,null=True)
    twitter_link=models.CharField(max_length=50,null=True)
    youtube_link=models.CharField(max_length=50,null=True)
    website_link=models.CharField(max_length=50,null=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
