from django import forms
from .models import Branch, Enterprise

class BaseForm(forms.ModelForm):
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user  # Garante que o usuário logado seja associado à criação
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class EnterpriseForm(BaseForm):
    class Meta:
        model = Enterprise
        fields = ['name', 'document']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'document': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'}),
        }

class BranchForm(BaseForm):
    class Meta:
        model = Branch
        fields = ['enterprise', 'name', 'document']
        widgets = {
            'enterprise': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Filial'}),
            'document': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'}),
        }
