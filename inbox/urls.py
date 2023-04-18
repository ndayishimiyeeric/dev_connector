from django.urls import path
from .views import create_conversation, conversation_list, conversation_detail

urlpatterns = [
    path("create/", create_conversation, name="create_conversation"),
    path("list/", conversation_list, name="conversation_list"),
    path("<str:pk>/", conversation_detail, name="conversation_detail"),
]
