from django.db import models


class Enterprise(models.Model):
    name = models.CharField(max_length=150)
    document = models.CharField('CPF/CNPJ', max_length=150)
    user = models.ForeignKey('accounts.USer', on_delete=models.CASCADE)
    
class Branches(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    document = models.CharField('CPF/CNPJ', max_length=150)
    user = models.ForeignKey('accounts.USer', on_delete=models.CASCADE)