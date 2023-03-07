from django.urls import path
from .views import projects, project,addProject,addPost
from .views import projects, project, createProject, updateProject, deleteProject


urlpatterns = [
    path("", projects, name="projects"),
    path("addProject", addProject, name="addproject"),
    path("addPost", addPost, name="addpost"),
    path("project/<int:pk>/", project, name="project"),
    path("", projects, name="projects"),
    path("project/<str:pk>/", project, name="project"),
    path("create-project/", createProject, name="create-project"),
    path("update-project/<str:pk>/", updateProject, name="update-project"),
    path("delete-project/<str:pk>/", deleteProject, name="delete-project")
]

    