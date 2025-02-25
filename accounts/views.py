from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth import login, authenticate
from .forms import CustomLoginForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
        else:
            print(form.errors) 
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})  
