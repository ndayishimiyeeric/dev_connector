from django.db import models

from authentication.models import User

# Create your models here.

class Degree(models.Model):
    name=models.CharField(max_length=50)



class Education(models.Model):
    school=models.CharField(max_length=50)
    field=models.CharField(max_length=50)
    description= models.TextField(max_length=200)
    date_from=models.DateField()
    date_to=models.DateField(null=True)
    is_current=models.BooleanField()
    degree=models.ForeignKey(Degree,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)





