from django.urls import path, include, re_path
from . import views
from users.views import CustomTokenVerifyView, CustomTokenRefreshView, CustomTokenObtainPairView, CustomProviderAuthView, LogoutView
from projects.views import get_project, get_projects

urlpatterns = [
    path('', views.get_routes, name="routes"),
    path('auth/', include('djoser.urls')),
    re_path(
        r'^o/(?P<provider>\S+)/$', CustomProviderAuthView.as_view()
    ),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view()),
    path('auth/jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('auth/jwt/verify/', CustomTokenVerifyView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('projects/', get_projects),
    path('projects/<str:pk>/', get_project),
]
