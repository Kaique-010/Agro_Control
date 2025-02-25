from .views import Menu
from django.urls import path


urlpatterns = [
    
    path("home", Menu, name="home")
    ]