from django.contrib import admin
from .models import User, Group, GroupPermission, UserGroup

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_owner')
    search_fields = ('email', 'name')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'enterprise')
    search_fields = ('name',)

class GroupPermissionAdmin(admin.ModelAdmin):
    list_display = ('group', 'permission')
    search_fields = ('group__name', 'permission__codename')

class UserGroupsAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    search_fields = ('user__email', 'group__name')

# Registrando corretamente os modelos no admin
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupPermission, GroupPermissionAdmin)  # ✅ Corrigido
admin.site.register(UserGroup, UserGroupsAdmin)
