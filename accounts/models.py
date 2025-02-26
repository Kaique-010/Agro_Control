from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from django.utils.translation import gettext_lazy as _
from companies.models import Enterprise


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Cria e retorna um usuário com email e senha."""
        if not email:
            raise ValueError(_('O campo Email deve ser preenchido'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria um superusuário com todas as permissões."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        user = self.create_user(email, password, **extra_fields)
        
        # Dar todas as permissões ao superusuário
        user.user_permissions.set(Permission.objects.all())
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    empresa = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios')
    filial = models.ForeignKey('companies.Branch', on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios')
    is_owner = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Para permitir acesso ao admin
    is_superuser = models.BooleanField(default=False)  # Para identificar superusuário
    is_active = models.BooleanField(default=True)  # Para permitir login

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Campos obrigatórios para criar superusuário

    objects = UserManager()

    def __str__(self):
        return self.email


class Group(models.Model):

    name = models.CharField(max_length=150)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GroupPermission(models.Model):
  
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, default=1)  

    def __str__(self):
        return f"{self.group.name} - {self.permission.codename}"  # ✅ Melhorado


class UserGroup(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.group.name}"



