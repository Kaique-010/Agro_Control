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

    def save(self,*args, **kwargs):
        self.descricao = self.descricao.upper()
        super().save(*args, **kwargs)

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
    
    def save(self,*args, **kwargs):
        self.descricao = self.descricao.upper()
        super().save(*args, **kwargs)

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
    
    def save(self,*args, **kwargs):
        self.descricao = self.descricao.upper()
        super().save(*args, **kwargs)
   


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
    tipo = models.CharField(max_length=10, choices=[('debito', 'Débito'), ('credito', 'Crédito'), ('projetos', 'Projetos'), ('extras','Extras')])

    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custos'
        ordering = [ 'codigo']
        db_table = 'centrosdecustos'
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            if self.filho:
                # Se o usuário escolheu um FILHO, o neto será criado abaixo dele
                self.pai = self.filho  # Define automaticamente o filho como pai

            if self.pai:
                ultimo_filho = self.pai.filhos.order_by('-codigo').first()
                if ultimo_filho:
                    try:
                        ultimo_numero = int(ultimo_filho.codigo.split('.')[-1]) + 1
                    except ValueError:
                        ultimo_numero = 1
                else:
                    ultimo_numero = 1
                self.codigo = f"{self.pai.codigo}.{str(ultimo_numero).zfill(3)}"
            else:
                prefixo = {'debito': '1', 'credito': '2', 'projetos': '3', 'extras': '4'}.get(self.tipo, '0')
                max_codigo = CentroDeCusto.objects.filter(codigo__startswith=prefixo).order_by('-codigo').first()
                if max_codigo:
                    try:
                        ultimo_numero = int(max_codigo.codigo.split('.')[0]) + 1
                    except ValueError:
                        ultimo_numero = int(prefixo)
                else:
                    ultimo_numero = int(prefixo)
                self.codigo = str(ultimo_numero)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.codigo})"


class PlanoDeContas(models.Model):
    TIPOS_CONTA = [
        ('ativos', 'Ativos'),
        ('passivos', 'Passivos'),
        ('receitas', 'Receitas'),
        ('despesas', 'Despesas'),
    ]

    MOVIMENTACAO = [
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
    ]

    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    tipo = models.CharField(max_length=10, choices=TIPOS_CONTA)
    movimento = models.CharField(max_length=7, choices=MOVIMENTACAO, default='debito')

    resumido = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name="expandido",
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = 'Plano de Contas'
        verbose_name_plural = 'Planos de Contas'
        ordering = ['codigo']
        db_table = 'planodecontas'

    def save(self, *args, **kwargs):
        if self.resumido:
            expandido_count = self.resumido.expandido.count() + 1
            self.codigo = f"{self.resumido.codigo}.{str(expandido_count).zfill(3)}"
        else:
            if self.tipo == 'ativos':
                prefixo = '1'
                self.movimento = 'debito'
            elif self.tipo == 'passivos':
                prefixo = '2'
                self.movimento = 'credito'
            elif self.tipo == 'receitas':
                prefixo = '3'
                self.movimento = 'credito'
            elif self.tipo == 'despesas':
                prefixo = '4'
                self.movimento = 'debito'
            else:
                raise ValueError("Tipo de conta inválido!")

            max_codigo = PlanoDeContas.objects.filter(codigo__startswith=prefixo).order_by('-codigo').first()

            if max_codigo and max_codigo.codigo:
                try:
                    ultimo_numero = int(max_codigo.codigo.split('.')[-1]) + 1
                except ValueError:
                    ultimo_numero = 1  # Se erro, inicia do 1
            else:
                ultimo_numero = 1  # Se não houver códigos anteriores, começa no 1

            self.codigo = f"{prefixo}.{str(ultimo_numero).zfill(3)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.movimento})"


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
    centro_de_custo = models.ForeignKey(CentroDeCusto, on_delete=models.CASCADE, null=True, blank=True, db_column='centro_de_custo')
    plano_de_contas = models.ForeignKey(PlanoDeContas, on_delete=models.CASCADE, blank=True, null=True, db_column='plano_de_contas')
    
    

    class Meta:
        verbose_name = 'Conta a Receber'
        verbose_name_plural = 'Contas a Receber'
        ordering = ['criado', 'id']
        db_table = 'contaareceber'
    
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
    centro_de_custo = models.ForeignKey(CentroDeCusto, on_delete=models.CASCADE, null=True, blank=True, db_column='centro_de_custo')
    plano_de_contas = models.ForeignKey(PlanoDeContas, on_delete=models.CASCADE, blank=True, null=True, db_column='plano_de_contas')
    


    class Meta:
        verbose_name = 'Conta a Pagar'
        verbose_name_plural = 'Contas a Pagar'
        ordering = ['criado', 'id']
        db_table = 'contaapagar'
    
    def __str__(self):
        return self.descricao
    