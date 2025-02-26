from django.contrib import admin
from .models import FormasPagamento, FormasRecebimento, ContaAPagar, ContaAReceber, Categorias, CentroDeCusto

class FormasPagamentoAdmin(admin.ModelAdmin):
    list_display = ('id','descricao',)
    search_fields = ('id','descricao',)

class FormasRecebimentoAdmin(admin.ModelAdmin):
    list_display = ('id','descricao',)
    search_fields = ('id','descricao',)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id','descricao',)
    search_fields = ('id','descricao',)

class ContasAPagarAdmin(admin.ModelAdmin):
    list_display = (
        'data_emissao', 'data_vencimento', 'documento', 
        'parcela', 'valor', 'data_pagamento', 'status_pagamento',
        'pessoas', 'categorias', 'observacoes', 'forma_pagamento',
    )
    search_fields = ('descricao', 'documento', 'pessoas__nome')
    list_filter = ('status_pagamento', 'forma_pagamento')

class ContasAReceberAdmin(admin.ModelAdmin):
    list_display = (
        'data_emissao', 'data_vencimento', 'documento', 
        'parcela', 'valor', 'data_recebimento', 'status_recebimento',
        'pessoas', 'categorias', 'observacoes', 'forma_recebimento',
    )
    search_fields = ('descricao', 'documento', 'pessoas__nome')
    list_filter = ('status_recebimento', 'forma_recebimento')
    


class CentroDeCustoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'tipo', 'pai')
    search_fields = ('nome', 'codigo')
    list_filter = ('tipo',)

admin.site.register(FormasPagamento, FormasPagamentoAdmin)
admin.site.register(FormasRecebimento, FormasRecebimentoAdmin)
admin.site.register(Categorias, CategoriaAdmin)
admin.site.register(ContaAPagar, ContasAPagarAdmin)
admin.site.register(ContaAReceber, ContasAReceberAdmin)
admin.site.register(CentroDeCusto, CentroDeCustoAdmin)





