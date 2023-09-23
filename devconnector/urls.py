from django.contrib import admin
from django.urls import path, include

# for serving media files in development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path(r'api/^auth/', include('djoser.urls')),
    path(r'api/^auth/', include('djoser.urls.jwt')),
    path("projects/", include("projects.urls")),
    path("", include("users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
