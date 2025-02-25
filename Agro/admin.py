# admin.py

from django.contrib import admin
from .models import (
    Fazenda,
    Talhao,
    CategoriaProduto,
    ProdutoAgro,
    EstoqueFazenda,
    MovimentacaoEstoque,
    AplicacaoInsumos,
    Animal,
    EventoAnimal,
    CicloFlorestal,
)

class BaseModelAdmin(admin.ModelAdmin):
    list_display = []  # Use uma lista vazia em vez de list
    search_fields = []  # Use uma lista vazia em vez de list
    list_filter = []  # Use uma lista vazia em vez de list

@admin.register(Fazenda)
class FazendaAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['nome', 'localizacao']
    search_fields = BaseModelAdmin.search_fields + ['nome', 'localizacao']

@admin.register(Talhao)
class TalhaoAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['nome', 'area', 'unidade_medida', 'fazenda']
    search_fields = BaseModelAdmin.search_fields + ['nome', 'fazenda__nome']

@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['nome']
    search_fields = BaseModelAdmin.search_fields + ['nome']

@admin.register(ProdutoAgro)
class ProdutoAgroAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['codigo', 'nome', 'categoria', 'unidade_medida', 'custo_medio']
    search_fields = BaseModelAdmin.search_fields + ['codigo', 'nome', 'categoria__nome']

@admin.register(EstoqueFazenda)
class EstoqueFazendaAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['fazenda', 'produto', 'quantidade', 'custo_medio_atualizado']
    search_fields = BaseModelAdmin.search_fields + ['fazenda__nome', 'produto__nome']

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['fazenda', 'produto', 'quantidade', 'tipo', 'data']
    search_fields = BaseModelAdmin.search_fields + ['fazenda__nome', 'produto__nome', 'tipo']

@admin.register(AplicacaoInsumos)
class AplicacaoInsumosAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['talhao', 'produto', 'quantidade_aplicada', 'data']
    search_fields = BaseModelAdmin.search_fields + ['talhao__nome', 'produto__nome']

@admin.register(Animal)
class AnimalAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['identificacao', 'raca', 'data_nascimento', 'sexo', 'peso_atual']
    search_fields = BaseModelAdmin.search_fields + ['identificacao', 'raca', 'fazenda__nome']

@admin.register(EventoAnimal)
class EventoAnimalAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['animal', 'tipo_evento', 'data_evento', 'custo']
    search_fields = BaseModelAdmin.search_fields + ['animal__identificacao', 'tipo_evento']

@admin.register(CicloFlorestal)
class CicloFlorestalAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ['talhao', 'cultura', 'data_plantio', 'volume_esperado', 'volume_real']
    search_fields = BaseModelAdmin.search_fields + ['talhao__nome', 'cultura']
