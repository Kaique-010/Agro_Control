import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from Pessoas.models import Pessoas
from System  import settings
from django.utils.translation import gettext_lazy as _
from companies.models import Enterprise


class Base(models.Model):
    empresa = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    criado = models.DateField('Criado em', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True
        


class FormasRecebimento(Base):
    
    TIPO_RECEBIMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'Pix'),
        ('boleto', 'Boleto'),
        ('transferencia', 'Transferência Bancária'),
        
    ]
    descricao = models.CharField('Tipo de Recebimento', max_length=25)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    
    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Forma de Recebimento'
        verbose_name_plural = 'Formas de Recebimento'
        ordering = ['criado', 'id']
        db_table = 'formasrecebimento'


class FormasPagamento(Base):
    
    descricao = models.CharField('Tipo de Pagamento', max_length=25)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['criado', 'id']
        db_table = 'formaspagamento'

class CategoriasFinanceiro(Base):
    descricao = models.CharField('Descrição', max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
       
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['criado', 'id']
        db_table = 'categoriasfinanceiro'
    
    def __str__(self):
        return self.descricao


class ContaAPagar(Base):
    documento = models.CharField('Documento',max_length=20)
    descricao = models.CharField('Descrição',max_length=255)
    parcela = models.IntegerField('Parcelas')
    valor = models.DecimalField('Valor',max_digits=10, decimal_places=2)
    data_emissao = models.DateField('Data de Emissão')
    data_vencimento = models.DateField('Vencimento')
    data_pagamento = models.DateField('Data de Pagamento', null=True, blank=True)
    status_pagamento = models.BooleanField('Status de Pagamento',default=False)
    pessoas = models.ForeignKey(Pessoas, on_delete=models.PROTECT, related_name='contas_a_pagar')
    categorias = models.ForeignKey(CategoriasFinanceiro, on_delete= models.PROTECT, max_length=100)
    observacoes = models.TextField('Observações',null=True, blank=True)
    forma_pagamento = models.ForeignKey(FormasPagamento, on_delete=models.SET_NULL, null=True, blank=True)
    


    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['criado', 'id']
        db_table = 'contaapagar'
    
    def __str__(self):
        return self.descricao
    
    


class ContaAReceber(Base):
    documento = models.CharField('Documento',max_length=20)
    descricao = models.CharField('Descrição',max_length=255)
    parcela = models.IntegerField('Parcelas')
    valor = models.DecimalField('Valor',max_digits=10, decimal_places=2)
    data_emissao = models.DateField('Data de Emissão')
    data_vencimento = models.DateField('Vencimento')
    data_recebimento = models.DateField('Data de Recebimento', null=True, blank=True)
    status_recebimento = models.BooleanField(default=False)
    pessoas = models.ForeignKey(Pessoas, on_delete=models.CASCADE, related_name='contas_a_receber')
    categorias = models.ForeignKey(CategoriasFinanceiro, on_delete= models.PROTECT, max_length=100)
    observacoes = models.TextField('Observações',null=True, blank=True)
    forma_recebimento = models.ForeignKey(FormasRecebimento, on_delete=models.SET_NULL, null=True, blank=True)
    

    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['criado', 'id']
        db_table = 'contaareceber'
    
    def __str__(self):
        return self.descricao
    


class GerarParcela(Base):
    
    class TipoParcela(models.TextChoices):
        PAGAR = "pagar", _("Pagar")
        RECEBER = "receber", _("Receber")

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    vencimento_inicial = models.DateField()
    tipo = models.CharField(max_length=10, choices=TipoParcela.choices)
    documento = models.PositiveIntegerField("Nº do documento")
    total_parcelas = models.PositiveIntegerField()
    descricao = models.CharField(max_length=255, blank=True, null=True)
    quitacao = models.ForeignKey(FormasRecebimento, on_delete=models.SET_NULL, null=True, blank=True)
    responsavel = models.ForeignKey(Pessoas, on_delete=models.CASCADE, related_name='gerarparcela')
    pagamento_total = models.BooleanField(default=False)
    pagamento_parcial = models.BooleanField(default=False)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Gerar Parcela'
        verbose_name_plural = 'Gerar Parcelas'
        ordering = ['criado', 'id']
        db_table = 'gerarparcelas'

    def __str__(self):
        return f"Parcela {self.documento}/{self.total_parcelas} - {self.tipo} - R$ {self.valor:.2f}"
    
    



class CentroDeCusto(Base):
    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=20, unique=True, editable=False)
    pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='filhos')
    filho = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='netos')
    tipo = models.CharField(max_length=10, choices=[('debito', 'Débito'), ('credito', 'Crédito')])

    def save(self, *args, **kwargs):
        # Lógica para gerar o código com base no pai e filho
        if self.pai:
            if self.filho:
                # Contar o número de netos (filhos do filho)
                self.codigo = f"{self.pai.codigo}.{self.filho.codigo}.{str(self.filho.netos.count() + 1).zfill(3)}"
            else:
                # Contar o número de filhos do pai
                self.codigo = f"{self.pai.codigo}.{str(self.pai.filhos.count() + 1).zfill(3)}"
        else:
            # Para centros de custo raiz
            if self.tipo == 'debito':
                max_codigo = CentroDeCusto.objects.filter(codigo__regex=r'^1(\.|\d)*$').order_by('-codigo').first()
                if not max_codigo:
                    self.codigo = '1'
                else:
                    self.codigo = str(int(max_codigo.codigo) + 1)
            else:  # Para crédito
                max_codigo = CentroDeCusto.objects.filter(codigo__regex=r'^2(\.|\d)*$').order_by('-codigo').first()
                if not max_codigo:
                    self.codigo = '2'
                else:
                    self.codigo = str(int(max_codigo.codigo) + 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.codigo})"
