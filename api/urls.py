from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name="routes"),
    path('projects/', views.get_products, name="projects"),
    path('projects/<str:pk>/', views.get_project, name="projects"),
]
