from django.urls import path

from .main_entry import main_entry
from .moderator_auth import moderator_auth

app_name = 'admin'

urlpatterns = [
    path("", main_entry, name="main"),
    path("@/<str:token>", moderator_auth, name="auth_moderator"),
]
