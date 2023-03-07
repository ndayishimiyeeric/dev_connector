from django.urls import path
from .views import profiles



urlpatterns = [
    path('', profiles, name='profiles'),
]