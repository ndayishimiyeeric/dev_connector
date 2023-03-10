from django.urls import path
from .views import profiles, profile



urlpatterns = [
    path('', profiles, name='profiles'),
    path("profile/<str:pk>/", profile, name='user-profile'),
]