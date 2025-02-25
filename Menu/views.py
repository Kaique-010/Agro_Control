from django.shortcuts import render



def Menu(request):
    'Hello World'
    return render(request, 'home.html')
