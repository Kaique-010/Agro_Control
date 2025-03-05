from django import forms
from .models import ContaAPagar, ContaAReceber, FormasPagamento, FormasRecebimento, CategoriasFinanceiro, CentroDeCusto
from .models import GerarParcela


class BaseForm(forms.ModelForm):
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            # Define o _request_user para que o modelo possa acessá-lo no save()
            instance._request_user = user  
            instance.atualizado_por = user
            if not instance.empresa_id:
                instance.empresa = user.empresa
           
        if commit:
            instance.save()
            self.save_m2m()
        return instance



class ContaAPagarForm(BaseForm):
    class Meta:
        model = ContaAPagar
        fields = [ 'status_pagamento','documento', 'descricao', 'parcela', 'valor',
                   'data_emissao', 'data_vencimento', 'data_pagamento', 'pessoas',
                   'categorias', 'observacoes',  'forma_pagamento', 'centro_de_custo', 'plano_de_contas']
        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'parcela': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Parcelas'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'pessoas': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações','rows': 1}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo': forms.Select(attrs={'class': 'form-control'}),
            'plano_de_contas': forms.Select(attrs={'class': 'form-control'}),
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas centros de custo do tipo 'Débito' e que são filhos (têm um pai)
        self.fields["centro_de_custo"].queryset = CentroDeCusto.objects.filter(tipo="debito").exclude(pai__isnull=True)
        # Filtra apenas planos de contas que não sejam pais (não tenham filhos)
        self.fields["plano_de_contas"].queryset = PlanoDeContas.objects.filter(expandido__isnull=True)


class ContaAReceberForm(BaseForm):
    class Meta:
        model = ContaAReceber
        fields = [ 'status_recebimento','documento', 'descricao', 'parcela', 'valor','data_emissao',
                  'data_vencimento', 'data_recebimento','pessoas', 'categorias', 'observacoes',
                  'forma_recebimento',  'centro_de_custo', 'plano_de_contas']
        
        widgets = {
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
            'parcela': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Parcelas'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Valor'}),
            'data_emissao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_recebimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'pessoas': forms.Select(attrs={'class': 'form-control'}),
            'categorias': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows':1}),
            'forma_recebimento': forms.Select(attrs={'class': 'form-control'}),
            'centro_de_custo': forms.Select(attrs={'class': 'form-control'}),
            'plano_de_contas': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas centros de custo do tipo 'Crédito' e que são filhos (têm um pai)
        self.fields["centro_de_custo"].queryset = CentroDeCusto.objects.filter(tipo="credito").exclude(pai__isnull=True)
        # Filtra apenas planos de contas que não sejam pais (não tenham filhos)
        self.fields["plano_de_contas"].queryset = PlanoDeContas.objects.filter(expandido__isnull=True)
            
            
class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Data Inicial', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Data Final', widget=forms.DateInput(attrs={'type': 'date'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ['%Y-%m-%d']
        self.fields['end_date'].input_formats = ['%Y-%m-%d']    






class CategoriaForm(BaseForm):
    class Meta:
        model = CategoriasFinanceiro
        fields = ['descricao'] 

    
    descricao = forms.CharField(max_length=255, required=False, label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1}))

    def clean_nome(self):
        nome = self.cleaned_data['descricao']
        if CategoriasFinanceiro.objects.filter(descricao='descricao').exists():
            raise forms.ValidationError("Esta categoria já existe.")
        return nome


class FormasRecebimentoForm(BaseForm):
    class Meta:
        model = FormasRecebimento
        fields = ['descricao']  

    descricao = forms.CharField(max_length=255, label='Descrição', widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 1}))

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        if FormasRecebimento.objects.filter(descricao=descricao).exists():
            raise forms.ValidationError("Esta forma de recebimento já existe.")
        return descricao




class FormasPagamentoForm(BaseForm):
    class Meta:
        model = FormasPagamento
        fields = ['descricao']  

    descricao = forms.CharField(max_length=255, label='Descrição', widget=forms.TextInput(attrs={'class': 'form-control'}))
    

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        if FormasPagamento.objects.filter(descricao=descricao).exists():
            raise forms.ValidationError("Esta forma de pagamento já existe.")
        return descricao



class GerarParcelasForm(BaseForm):
    class Meta:
        model = GerarParcela
        fields = [
            "valor",
            "vencimento_inicial",
            "tipo",
            "documento",
            "total_parcelas",
            "descricao",
            "quitacao",
            "responsavel",
            "pagamento_total",
            "pagamento_parcial",
            "valor_pago"
        ]
        widgets = {
            "valor": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Valor total"}),
            "vencimento_inicial": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "documento": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Número do documento"}),
            "total_parcelas": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Total de parcelas"}),
            "descricao": forms.TextInput(attrs={"class": "form-control", "placeholder": "Descrição (opcional)"}),
            "quitacao": forms.Select(attrs={"class": "form-control"}),
            "responsavel": forms.Select(attrs={"class": "form-control"}),
            "pagamento_total": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "pagamento_parcial": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "valor_pago": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Valor Pago"}),
        }
        



class CentroDeCustoForm(BaseForm):
    class Meta:
        model = CentroDeCusto
        fields = ['nome', 'tipo', 'pai', 'filho']  
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'tipo'}),
            'pai': forms.Select(attrs={'class': 'form-control', 'placeholder': 'movimento'}),
            'filho': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limitar a seleção de centros de custo para os pais
        self.fields['pai'].queryset = CentroDeCusto.objects.filter(pai__isnull=True)  # Pais (centros de custo raiz)
        
        # Limitar a seleção de filhos para os centros de custo que já são filhos de um pai
        self.fields['filho'].queryset = CentroDeCusto.objects.filter(pai__isnull=False)  # Filhos (centros de custo filhos)




from django import forms
from .models import PlanoDeContas

class PlanoDeContasForm(forms.ModelForm):
    class Meta:
        model = PlanoDeContas
        fields = ['nome', 'tipo', 'movimento', 'resumido']  # Defina os campos que deseja exibir no formulário
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'tipo': forms.Select(choices=PlanoDeContas.TIPOS_CONTA, attrs={'class': 'form-control', 'placeholder': 'tipo'}),
            'movimento': forms.Select(choices=PlanoDeContas.MOVIMENTACAO, attrs={'class': 'form-control', 'placeholder': 'movimento'}),
            'resumido': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Descrição'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize widgets, labels, etc., se necessário

    def clean(self):
        cleaned_data = super().clean()

        tipo = cleaned_data.get('tipo')
        movimento = cleaned_data.get('movimento')

        # Verifique se o movimento está correto com base no tipo
        if tipo in ['ativos', 'despesas'] and movimento != 'debito':
            self.add_error('movimento', 'Para Ativos e Despesas, o movimento deve ser Débito.')
        elif tipo in ['passivos', 'receitas'] and movimento != 'credito':
            self.add_error('movimento', 'Para Passivos e Receitas, o movimento deve ser Crédito.')

        return cleaned_data
