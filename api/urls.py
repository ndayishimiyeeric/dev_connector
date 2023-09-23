from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.get_routes, name="routes"),
    path('auth/', include('djoser.urls')),
    re_path(
        r'^o/(?P<provider>\S+)/$', views.CustomProviderAuthView.as_view()
    ),
    path('auth/jwt/create/', views.CustomTokenObtainPairView.as_view()),
    path('auth/jwt/refresh/', views.CustomTokenRefreshView.as_view()),
    path('auth/jwt/verify/', views.CustomTokenVerifyView.as_view()),
    path('auth/logout/', views.LogoutView.as_view()),
    path('projects/', views.get_products, name="projects"),
    path('projects/<str:pk>/', views.get_project, name="projects"),
]
