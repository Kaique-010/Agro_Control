from django import forms
from .models import Fazenda, Talhao, CategoriaProduto, ProdutoAgro, EstoqueFazenda, MovimentacaoEstoque, AplicacaoInsumos, Animal, EventoAnimal, CicloFlorestal


class BaseForm(forms.ModelForm):
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            # Define o _request_user para que o modelo possa acessá-lo no save()
            instance._request_user = user  
            instance.atualizado_por = user
            if not instance.empresa_id:
                instance.empresa = user.empresa
            if not instance.filial_id:
                instance.filial = user.filial
        if commit:
            instance.save()
            self.save_m2m()
        return instance





class FazendaForm(BaseForm):
    class Meta:
        model = Fazenda
        fields = ['nome', 'localizacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome da Fazenda'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Localização'}),
           
        }
    
   
        


class TalhaoForm(BaseForm):
    class Meta:
        model = Talhao
        fields = ['fazenda', 'nome', 'area', 'unidade_medida']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome do Talhão'}),
            'area': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Área'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Unidade de Medida'}),
           
        }
    
   


class CategoriaProdutoForm(BaseForm):
    class Meta:
        model = CategoriaProduto
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome da Categoria'}),
       
        }

   


class ProdutoAgroForm(BaseForm):
    class Meta:
        model = ProdutoAgro
        exclude = ['codigo']
        fields = [ 'nome', 'categoria', 'unidade_medida', 'descricao', 'custo_medio']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Código'}),
            'nome': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Nome do Produto'}),
            'categoria': forms.Select(attrs={'class': 'form-control col-6'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Unidade de Medida'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Descrição'}),
            'custo_medio': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Médio'}),
           
        }

    
    

class EstoqueFazendaForm(BaseForm):
    class Meta:
        model = EstoqueFazenda
        fields = ['fazenda', 'produto', 'quantidade', 'custo_medio_atualizado']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'produto': forms.Select(attrs={'class': 'form-control col-6'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Quantidade'}),
            'custo_medio_atualizado': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Médio Atualizado'}),
          
        }


    

class MovimentacaoEstoqueForm(BaseForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['fazenda', 'produto', 'quantidade', 'tipo', 'documento_referencia', 'motivo', 'custo_unitario']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'produto': forms.Select(attrs={'class': 'form-control col-6'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Quantidade'}),
            'tipo': forms.Select(attrs={'class': 'form-control col-6'}),
            'documento_referencia': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Documento de Referência'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Motivo'}),
            'custo_unitario': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Unitário'}),
           
        }
    
    


class AplicacaoInsumosForm(BaseForm):
    class Meta:
        model = AplicacaoInsumos
        fields = ['empresa' ,'filial','talhao', 'produto', 'quantidade_aplicada', 
                  'observacoes']
        widgets = {
            'talhao': forms.Select(attrs={'class': 'form-control col-6'}),
            'produto': forms.Select(attrs={'class': 'form-control col-6'}),
            'quantidade_aplicada': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Quantidade Aplicada'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Observações'}),
  
        }

  
    
    

class AnimalForm(BaseForm):
    class Meta:
        model = Animal
        fields = ['fazenda', 'identificacao', 'raca', 'data_nascimento', 'sexo', 'peso_atual', 'observacoes']
        widgets = {
            'fazenda': forms.Select(attrs={'class': 'form-control col-6'}),
            'identificacao': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Identificação'}),
            'raca': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Raça'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data de Nascimento', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-control col-6'}),
            'peso_atual': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Peso Atual'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Observações'}),
    
        }




class EventoAnimalForm(BaseForm):
    class Meta:
        model = EventoAnimal
        fields = ['animal', 'tipo_evento', 'data_evento', 'custo', 'descricao']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control col-6'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control col-6'}),
            'data_evento': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data do Evento', 'type': 'date'}),
            'custo': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Descrição'}),
           
           
        }




class CicloFlorestalForm(BaseForm):
    class Meta:
        model = CicloFlorestal
        fields = ['talhao', 'cultura', 'data_plantio', 'data_previsao_colheita', 'data_colheita', 'volume_esperado', 'volume_real', 'custo_total', 'observacoes']
        widgets = {
            'talhao': forms.Select(attrs={'class': 'form-control col-6'}),
            'cultura': forms.TextInput(attrs={'class': 'form-control col-6', 'placeholder': 'Cultura'}),
            'data_plantio': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data de Plantio', 'type': 'date'}),
            'data_previsao_colheita': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data Previsão Colheita', 'type': 'date'}),
            'data_colheita': forms.DateInput(attrs={'class': 'form-control col-6', 'placeholder': 'Data de Colheita', 'type': 'date'}),
            'volume_esperado': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Volume Esperado'}),
            'volume_real': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Volume Real'}),
            'custo_total': forms.NumberInput(attrs={'class': 'form-control col-6', 'placeholder': 'Custo Total'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control col-6', 'placeholder': 'Observações'}),
           
        }

  