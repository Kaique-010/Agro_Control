# admin.py

from django.contrib import admin
from .models import Enterprise, Branch

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('name', 'document', 'user')
    search_fields = ('name', 'document')

class BranchesAdmin(admin.ModelAdmin):
    list_display = ('name', 'document', 'enterprise', 'user')
    search_fields = ('name', 'document', 'enterprise__name')

# Registrando os modelos no admin
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Branch, BranchesAdmin)
