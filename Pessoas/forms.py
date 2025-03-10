from django import forms

from Agenda.models import Base
from . import models

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



class Pessoas(BaseForm):
    class Meta:
        model = models.Pessoas
        fields = ['nome', 'rg', 'cpf', 'cnpj', 'ie', 'telefone', 'cep', 'logradouro', 'numero', 'email', 'bairro', 'cidade', 'estado', 'classificacao', 'foto'] 

        widgets = {
            'classificacao': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF', 'maxlength': '14'}),
            'rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RG'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ', 'maxlength': '18'}),
            'ie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'maxlength': '15'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'maxlength': '9'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'obs': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 4}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_nome(self):
        data = self.cleaned_data.get('nome')
        return data.upper() if data else data

    def clean_cpf(self):
        data = self.cleaned_data.get('cpf')
        return data.upper() if data else data

    def clean_rg(self):
        data = self.cleaned_data.get('rg')
        return data.upper() if data else data

    def clean_cnpj(self):
        data = self.cleaned_data.get('cnpj')
        return data.upper() if data else data

    def clean_ie(self):
        data = self.cleaned_data.get('ie')
        return data.upper() if data else data

    def clean_telefone(self):
        data = self.cleaned_data.get('telefone')
        return data.upper() if data else data
