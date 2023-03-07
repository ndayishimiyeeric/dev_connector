from django.db import models
from authentication.models import User

# Create your models here.

class Experience(models.Model):
    title=models.CharField(max_length=200)
    company=models.CharField(max_length=100)
    location=models.CharField(max_length=50)
    description=models.TextField(max_length=200)
    date_from=models.DateField()
    date_to=models.DateField(null=True)
    is_current=models.BooleanField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="experiences")

