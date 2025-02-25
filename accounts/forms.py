from django import forms
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ['username', 'password']
        
