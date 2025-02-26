from django.db import models
from django.conf import settings

class Enterprise(models.Model):
    name = models.CharField(max_length=150)
    document = models.CharField('CPF/CNPJ', max_length=18, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enterprises")

    def __str__(self):
        return self.name

class Branch(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=150)
    document = models.CharField('CPF/CNPJ', max_length=18, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="branches")

    def __str__(self):
        return self.name
