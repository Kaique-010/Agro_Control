from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from companies.models import Branch, Enterprise



class BaseModel(models.Model):
    empresa = models.ForeignKey(Enterprise, on_delete=models.CASCADE, db_index=True)
    filial = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    atualizado_por = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_atualizacoes"
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Garante que o usuário responsável seja registrado ao salvar"""
        if hasattr(self, '_request_user') and self._request_user:
            if not self.atualizado_por:
                self.atualizado_por = self._request_user
            if not self.empresa_id:
                self.empresa = self._request_user.empresa
            if not self.filial_id:
                self.filial = self._request_user.filial
        super().save(*args, **kwargs)

class Fazenda(BaseModel):
    nome = models.CharField(max_length=255, db_index=True)
    localizacao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'fazendas'

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()  # Atribuir o valor em maiúsculas
        self.localizacao = self.localizacao.upper() if self.localizacao else None  # Verifica se não é None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Fazenda {self.nome}'


class Talhao(BaseModel):
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='talhoes')
    nome = models.CharField(max_length=255, db_index=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Área do talhão (pode ser em hectares ou m²)")
    unidade_medida = models.CharField(max_length=20, default="hectares", help_text="Unidade de medida da área (ex: hectares, m²)")

    class Meta:
        db_table = 'talhoes'

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        self.unidade_medida = self.unidade_medida.upper()  # Atribuir o valor em maiúsculas
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.fazenda.nome})"


class CategoriaProduto(BaseModel):
    nome = models.CharField(max_length=255, unique=True, db_index=True)

    class Meta:
        db_table = 'categorias_produtos'

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class ProdutoAgro(BaseModel):
    codigo = models.CharField(max_length=100, unique=True, db_index=True)
    nome = models.CharField(max_length=255, db_index=True)
    categoria = models.ForeignKey(CategoriaProduto, on_delete=models.PROTECT)
    unidade_medida = models.CharField(max_length=50)  # Ex: kg, litro, saco
    descricao = models.TextField(blank=True, null=True)
    custo_medio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        help_text="Custo médio do produto"
    )

    class Meta:
        db_table = 'produtos_agro'
        
    
    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        self.unidade_medida = self.unidade_medida.upper()
        self.descricao = self.descricao.upper() if self.descricao else None  # Verifica se não é None
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.categoria})"

    
    

class EstoqueFazenda(BaseModel):
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(ProdutoAgro, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_medio_atualizado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        help_text="Custo médio atualizado com base nas movimentações"
    )

    class Meta:
        unique_together = ('fazenda', 'produto')
        db_table = 'estoque_fazenda'

    def __str__(self):
        return f"{self.fazenda} - {self.produto}: {self.quantidade}"




class MovimentacaoEstoque(BaseModel):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name='movimentacoes')
    produto = models.ForeignKey(ProdutoAgro, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)
    documento_referencia = models.CharField(max_length=255, blank=True, null=True)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    custo_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Custo unitário na movimentação (para atualização do custo médio)"
    )
    
    class Meta:
        db_table = 'movimentacao_estoque'
    
    def __str__(self):
        return f"{self.fazenda} - {self.produto} ({self.tipo} de {self.quantidade}) em {self.data}"
    

    
    

class AplicacaoInsumos(BaseModel):
    talhao = models.ForeignKey(Talhao, on_delete=models.CASCADE, related_name='aplicacoes_insumos')
    produto = models.ForeignKey(ProdutoAgro, on_delete=models.CASCADE)
    quantidade_aplicada = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Quantidade de insumo aplicada"
    )
    data = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True, null=True)
    
    
    class Meta:
        db_table = 'aplicacao_insumos'
    
    def __str__(self):
        return f"Aplicação de {self.produto} no {self.talhao} em {self.data}"



class Animal(BaseModel):
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE, related_name="animais")
    identificacao = models.CharField(
        max_length=100, 
        unique=True, 
        help_text="Número de identificação ou tag do animal"
    )
    raca = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    peso_atual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
   
    class Meta:
        db_table = 'animais'
    
    def __str__(self):
        return f"{self.identificacao} ({self.fazenda.nome})"
    
    

class EventoAnimal(BaseModel):
    EVENTO_CHOICES = [
        ('nascimento', 'Nascimento'),
        ('vacinacao', 'Vacinação'),
        ('engorda', 'Engorda'),
        ('abate', 'Abate'),
        ('venda', 'Venda'),
        # Outros eventos podem ser adicionados conforme a necessidade
    ]
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="eventos")
    tipo_evento = models.CharField(max_length=50, choices=EVENTO_CHOICES)
    data_evento = models.DateField()
    custo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Custo associado a esse evento (se aplicável)"
    )
    descricao = models.TextField(blank=True, null=True)
    
    
    class Meta:
        db_table = 'eventos_animais'
    
    def __str__(self):
        return f"{self.animal.identificacao} - {self.get_tipo_evento_display()} em {self.data_evento}"



class CicloFlorestal(BaseModel):
    talhao = models.ForeignKey(Talhao, on_delete=models.CASCADE, related_name="ciclos_florestais")
    cultura = models.CharField(
        max_length=255, 
        help_text="Tipo de cultura florestal (ex: Eucalipto, Pinus)"
    )
    data_plantio = models.DateField()
    data_previsao_colheita = models.DateField(blank=True, null=True)
    data_colheita = models.DateField(blank=True, null=True)
    volume_esperado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Volume esperado da colheita (em m³ ou outra unidade)"
    )
    volume_real = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Volume efetivamente colhido"
    )
    custo_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Custo total do ciclo (produção, insumos, mão de obra, etc.)"
    )
    observacoes = models.TextField(blank=True, null=True)
    
    
    class Meta:
        db_table = 'ciclos_florestais'
    
    def __str__(self):
        return f"{self.cultura} no {self.talhao} - Plantado em {self.data_plantio}"

