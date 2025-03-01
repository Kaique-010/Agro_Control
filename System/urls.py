
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('Agenda.urls')),
    path('', include('Agro.urls')),
    path('', include('companies.urls')),
    path('', include('Financeiro.urls')),
    path('', include('Menu.urls')),
    path('', include('Pessoas.urls')),
]
