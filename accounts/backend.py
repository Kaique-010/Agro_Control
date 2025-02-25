from django.contrib.auth.backends import ModelBackend
from accounts.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(f"Tentativa de login: Email: {email}, Senha: {password}")  # Para depuração
        if email is None or password is None:
            print("Email ou senha não fornecidos.")
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print("Falha na autenticação: usuário não encontrado.")
            return None
        if user.check_password(password):
            return user
        print("Falha na autenticação: senha incorreta.")
        return None
