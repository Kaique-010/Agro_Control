from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from accounts.models import User
from companies.models import Enterprise, Employee
from utils import validate_not_empty


class Authentication:
    def signin(self, email=None, password=None) -> User:
       
        exception_auth = AuthenticationFailed("E-mail e/ou Senha Incorretos")

    
        user = User.objects.filter(email=email).first()
        if not user or not check_password(password, user.password):
            raise exception_auth

        return user

    @transaction.atomic
    def signup(self, name, email, password, type_account='owner', company_id=None) -> dict:

        validate_not_empty(name, "Nome")
        validate_not_empty(email, "Email")
        validate_not_empty(password, "Senha")

        if type_account not in ['owner', 'employee']:
            raise APIException("O tipo de conta deve ser 'owner' ou 'employee'.")

        if User.objects.filter(email=email).exists():
            raise APIException("Este e-mail já está cadastrado!")

        if type_account == 'employee' and not company_id:
            raise APIException("O ID da empresa é obrigatório para funcionários.")


        password_hashed = make_password(password)
        user = User.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=(type_account == 'owner')
        )

        
        if type_account == 'owner':
            enterprise = Enterprise.objects.create(name="Nome da Empresa", user_id=user.id)
        elif type_account == 'employee':
            Employee.objects.create(enterprise_id=company_id, user_id=user.id)

   
        return {
            "user_id": user.id,
            "email": user.email,
            "type_account": type_account,
        }
