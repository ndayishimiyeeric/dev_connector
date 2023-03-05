from django.db import models
import uuid
from authentication.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200,null=True)
    description = models.TextField(blank=True)
    source_code = models.URLField(null=True, blank=True, max_length=2000)
    live_preview = models.URLField(null=True, blank=True, max_length=2000)
    image=models.ImageField(upload_to="photos/projects/",null=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
