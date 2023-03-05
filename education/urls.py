
from django.urls import path

from education.views import *

urlpatterns=[
    path("addEducation",addEduction,name="addEducation")
]