from django.urls import path
from .views import login_view, LogoutView

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),


]
