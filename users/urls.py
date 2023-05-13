from django.urls import path
from .views import profile, userLogin, userLogout, userRegister, profiles, editProfile, feed, addExperience, \
    addEducation, createSkill, deleteSkill, updateSkill, deleteExperience, updateExperience, deleteEducation, \
    updateEducation, follow, unfollow

urlpatterns = [
    path("profile/<str:pk>/?tab=about/", profile, name="user-profile"),
    path("profile/<str:pk>/?tab=projects/", profile, name="user-projects"),
    path("profile/<str:pk>/?tab=followers/", profile, name="user-followers"),
    path("profile/<str:pk>/?tab=following/", profile, name="user-following"),
    path("", profiles, name="profiles"),
    path("edit-profile/", editProfile, name="edit-profile"),
    path("add-experience/", addExperience, name="add-experience"),
    path("add-education/", addEducation, name="add-education"),
    path("create-skill/", createSkill, name="create-skill"),
    path("delete-skill/<str:pk>/", deleteSkill, name="delete-skill"),
    path("update-skill/<str:pk>/", updateSkill, name="update-skill"),
    path("delete-experience/<str:pk>/", deleteExperience, name="delete-experience"),
    path("update-experience/<str:pk>/", updateExperience, name="update-experience"),
    path("delete-education/<str:pk>/", deleteEducation, name="delete-education"),
    path("update-education/<str:pk>/", updateEducation, name="update-education"),

    path("login/", userLogin, name="login"),
    path("logout/", userLogout, name="logout"),
    path("register/", userRegister, name="register"),

    path("follow/<str:pk>/", follow, name="follow"),
    path("unfollow/<str:pk>/", unfollow, name="unfollow"),

    path("feed/", feed, name="feed"),

    path('inbox', feed, name='inbox'),
]
