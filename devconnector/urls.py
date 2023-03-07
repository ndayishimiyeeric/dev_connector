from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from authentication import views
from profil import views as pv

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("projects.urls")),
    path("login",views.login_page,name="authentication"),
    path("register",views.register,name="register"),
    path('logout',views.logout_user,name="logout"),
    path("education/",include("education.urls")),
    path('my_profile',pv.my_profil,name="my_profil"),
    path("home-page",pv.my_home_page,name="home_page")
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)