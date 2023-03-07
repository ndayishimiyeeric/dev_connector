from django.urls import path
from .views import projects, project,addProject,addPost

urlpatterns = [
    path("", projects, name="projects"),
    path("addProject", addProject, name="addproject"),
    path("addPost", addPost, name="addpost"),
    path("project/<int:pk>/", project, name="project"),
]