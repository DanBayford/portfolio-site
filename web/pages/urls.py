from django.urls import path
from .views import toggle_dark_mode

urlpatterns = [path("", toggle_dark_mode, name="toggle-dark-mode")]
