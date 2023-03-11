from django.urls import path
from .views import profiles, profile, userLogin, userLogout, userWelcome, userRegister, userDashboard



urlpatterns = [
    path('', profiles, name='profiles'),
    path("profile/<str:pk>/", profile, name='user-profile'),
    path("dashboard/", userDashboard, name="dashboard"),

    path('login/', userLogin, name='login'),
    path('register/', userRegister, name='register'),
    path('logout/', userLogout, name='logout'),
    path('welcome/', userWelcome, name='welcome'),
]