from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.get_routes, name="routes"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('projects/', views.get_products, name="projects"),
    path('projects/<str:pk>/', views.get_project, name="projects"),
]
