from django.urls import path
from .views import profiles, profile, userLogin, userLogout, userWelcome, userRegister, userDashboard, editProfile, \
    createSkill, updateSkill, deleteSkill, addExperience, updateExperience, deleteExperience

urlpatterns = [
    path('', profiles, name='profiles'),
    path("profile/<str:pk>/", profile, name='user-profile'),
    path("dashboard/", userDashboard, name="dashboard"),
    path('edit-profile/', editProfile, name='edit-profile'),
    path('create-skill/', createSkill, name='create-skill'),
    path('update-skill/<str:pk>/', updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', deleteSkill, name="delete-skill"),
    path('add-experience/', addExperience, name='add-experience'),
    path('update-experience/<str:pk>/', updateExperience, name='update-experience'),
    path('delete-experience/<str:pk>/', deleteExperience, name='delete-experience'),

    path('login/', userLogin, name='login'),
    path('register/', userRegister, name='register'),
    path('logout/', userLogout, name='logout'),
    path('welcome/', userWelcome, name='welcome'),
]
