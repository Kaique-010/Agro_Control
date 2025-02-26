from django.db import IntegrityError
from django.forms import ValidationError
from django.http import Http404, HttpResponse
from django.core.exceptions import PermissionDenied
import csv
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import CategoriaProduto, Fazenda, Talhao, ProdutoAgro, EstoqueFazenda, MovimentacaoEstoque, AplicacaoInsumos, Animal, EventoAnimal, CicloFlorestal
from .forms import CategoriaProdutoForm, FazendaForm, TalhaoForm, ProdutoAgroForm, EstoqueFazendaForm, MovimentacaoEstoqueForm, AplicacaoInsumosForm, AnimalForm, EventoAnimalForm, CicloFlorestalForm



class FazendaListView( ListView):
    model = Fazenda
    template_name = "fazenda_list.html"
    context_object_name = 'fazendas'
    
  

class FazendaCreateView( CreateView):
    model = Fazenda
    form_class = FazendaForm
    template_name = "agro/fazenda_form.html"
    success_url = reverse_lazy("fazenda_list")
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)
    
    


class FazendaUpdateView( UpdateView):
    model = Fazenda
    form_class = FazendaForm
    template_name = "agro/fazenda_form.html"
    success_url = reverse_lazy("fazenda_list")


class FazendaDeleteView( DeleteView):
    model = Fazenda
    template_name = "agro/fazenda_confirm_delete.html"
    success_url = reverse_lazy("fazenda_list")



# Talhão Views
class TalhaoListView( ListView):
    model = Talhao
    template_name = "agro/talhao_list.html"
    context_object_name = 'talhoes'


class TalhaoCreateView( CreateView):
    model = Talhao
    form_class = TalhaoForm
    template_name = "agro/talhao_form.html"
    success_url = reverse_lazy("talhao_list")
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)



class TalhaoUpdateView( UpdateView):
    model = Talhao
    form_class = TalhaoForm
    template_name = "agro/talhao_form.html"
    success_url = reverse_lazy("talhao_list")
    


class TalhaoDeleteView( DeleteView):
    model = Talhao
    template_name = "agro/talhao_confirm_delete.html"
    success_url = reverse_lazy("talhao_list")


# Produto Agro Views
class ProdutoAgroListView( ListView):
    model = ProdutoAgro
    template_name = "agro/produtoagro_list.html"


class ProdutoAgroCreateView( CreateView):
    model = ProdutoAgro
    form_class = ProdutoAgroForm
    template_name = "agro/produtoagro_form.html"
    success_url = reverse_lazy("produtoagro_list")
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)


class ProdutoAgroUpdateView( UpdateView):
    model = ProdutoAgro
    form_class = ProdutoAgroForm
    template_name = "agro/produtoagro_form.html"
    success_url = reverse_lazy("produtoagro_list")


class ProdutoAgroDeleteView( DeleteView):
    model = ProdutoAgro
    template_name = "agro/produtoagro_confirm_delete.html"
    success_url = reverse_lazy("produtoagro_list")


# Estoque Fazenda Views
class EstoqueFazendaListView( ListView):
    model = EstoqueFazenda
    template_name = "agro/estoquefazenda_list.html"


class EstoqueFazendaCreateView( CreateView):
    model = EstoqueFazenda
    form_class = EstoqueFazendaForm
    template_name = "agro/estoquefazenda_form.html"
    success_url = reverse_lazy("estoquefazenda_list")
    
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)



class EstoqueFazendaUpdateView( UpdateView):
    model = EstoqueFazenda
    form_class = EstoqueFazendaForm
    template_name = "agro/estoquefazenda_form.html"
    success_url = reverse_lazy("estoquefazenda_list")


class EstoqueFazendaDeleteView( DeleteView):
    model = EstoqueFazenda
    template_name = "agro/estoquefazenda_confirm_delete.html"
    success_url = reverse_lazy("estoquefazenda_list")


# Movimentação Estoque Views
class MovimentacaoEstoqueListView( ListView):
    model = MovimentacaoEstoque
    template_name = "agro/movimentacaoestoque_list.html"


class MovimentacaoEstoqueCreateView( CreateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "agro/movimentacaoestoque_form.html"
    success_url = reverse_lazy("movimentacaoestoque_list")
    
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)


class MovimentacaoEstoqueUpdateView( UpdateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "agro/movimentacaoestoque_form.html"
    success_url = reverse_lazy("movimentacaoestoque_list")



class MovimentacaoEstoqueDeleteView( DeleteView):
    model = MovimentacaoEstoque
    template_name = "agro/movimentacaoestoque_confirm_delete.html"
    success_url = reverse_lazy("movimentacaoestoque_list")


# Aplicacao Insumos Views
class AplicacaoInsumosListView( ListView):
    model = AplicacaoInsumos
    template_name = "agro/aplicacaoinsumos_list.html"


class AplicacaoInsumosCreateView( CreateView):
    model = AplicacaoInsumos
    form_class = AplicacaoInsumosForm
    template_name = "agro/aplicacaoinsumos_form.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)



class AplicacaoInsumosUpdateView( UpdateView):
    model = AplicacaoInsumos
    form_class = AplicacaoInsumosForm
    template_name = "agro/aplicacaoinsumos_form.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")



class AplicacaoInsumosDeleteView( DeleteView):
    model = AplicacaoInsumos
    template_name = "agro/aplicacaoinsumos_confirm_delete.html"
    success_url = reverse_lazy("aplicacaoinsumos_list")


# Animal Views
class AnimalListView( ListView):
    model = Animal
    template_name = "agro/animal_list.html"


class AnimalCreateView( CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = "agro/animal_form.html"
    success_url = reverse_lazy("animal_list")
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)



class AnimalUpdateView( UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = "agro/animal_form.html"
    success_url = reverse_lazy("animal_list")



class AnimalDeleteView( DeleteView):
    model = Animal
    template_name = "agro/animal_confirm_delete.html"
    success_url = reverse_lazy("animal_list")
    
    

# Evento Animal Views
class EventoAnimalListView( ListView):
    model = EventoAnimal
    template_name = "agro/eventoanimal_list.html"


class EventoAnimalCreateView( CreateView):
    model = EventoAnimal
    form_class = EventoAnimalForm
    template_name = "agro/eventoanimal_form.html"
    success_url = reverse_lazy("eventoanimal_list")
    
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)


class EventoAnimalUpdateView( UpdateView):
    model = EventoAnimal
    form_class = EventoAnimalForm
    template_name = "agro/eventoanimal_form.html"
    success_url = reverse_lazy("eventoanimal_list")


class EventoAnimalDeleteView( DeleteView):
    model = EventoAnimal
    template_name = "agro/eventoanimal_confirm_delete.html"
    success_url = reverse_lazy("eventoanimal_list")


# Ciclo Florestal Views
class CicloFlorestalListView( ListView):
    model = CicloFlorestal
    template_name = "agro/cicloflorestal_list.html"


class CicloFlorestalCreateView( CreateView):
    model = CicloFlorestal
    form_class = CicloFlorestalForm
    template_name = "agro/cicloflorestal_form.html"
    success_url = reverse_lazy("cicloflorestal_list")
    
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)


class CicloFlorestalUpdateView( UpdateView):
    model = CicloFlorestal
    form_class = CicloFlorestalForm
    template_name = "agro/cicloflorestal_form.html"
    success_url = reverse_lazy("cicloflorestal_list")


class CicloFlorestalDeleteView( DeleteView):
    model = CicloFlorestal
    template_name = "agro/cicloflorestal_confirm_delete.html"
    success_url = reverse_lazy("cicloflorestal_list")



class CategoriaProdutoListView( ListView):
    model = CategoriaProduto
    template_name = "agro/categoria_produto_list.html"
    context_object_name = 'categorias'



class CategoriaProdutoCreateView( CreateView):
    model = CategoriaProduto
    form_class = CategoriaProdutoForm
    template_name = "agro/categoria_produto_form.html"
    success_url = reverse_lazy("categoria_produto_list")
    
    def form_valid(self, form):
        try:
            form.save(user=self.request.user)
            return super().form_valid(form)
        except IntegrityError as e:
            if 'categorias_produtos_nome_key' in str(e):
                form.add_error("nome", "Já Existe uma categoria com este nome.")
            else:
                form.add_error(None, "Erro ao salvar a categoria. Tente novamente")
            return self.form_invalid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Corrija os erros abaixo e tente Novamente")
        return super().form_invalid(form)

    
            


class CategoriaProdutoUpdateView( UpdateView):
    model = CategoriaProduto
    form_class = CategoriaProdutoForm
    template_name = "agro/categoria_produto_form.html"
    success_url = reverse_lazy("categoria_produto_list")

class CategoriaProdutoDeleteView( DeleteView):
    model = CategoriaProduto
    template_name = "agro/categoria_produto_confirm_delete.html"
    success_url = reverse_lazy("categoria_produto_list")





# Relatório Movimentações
class RelatorioMovimentacoesView( ListView):
    model = MovimentacaoEstoque
    template_name = "agro/relatorio_movimentacoes.html"
    context_object_name = "movimentacoes"
    
    def get_queryset(self):
        queryset = MovimentacaoEstoque.objects.using(self.db_name).filter(estoque__fazenda__licenca=self.get_license())
        data_inicial = self.request.GET.get('data_inicial')
        data_final = self.request.GET.get('data_final')
        tipo = self.request.GET.get('tipo')

        if data_inicial and data_final:
            queryset = queryset.filter(data__range=[data_inicial, data_final])
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset

    def get(self, request, *args, **kwargs):
        if request.GET.get('exportar') == 'true':
            return self.exportar_movimentacoes()
        return super().get(request, *args, **kwargs)

    def exportar_movimentacoes(self):
        movimentacoes = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="movimentacoes.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Data', 'Tipo', 'Produto', 'Quantidade', 'Observações'])

        for movimentacao in movimentacoes:
            writer.writerow([movimentacao.data, movimentacao.tipo, movimentacao.produto, movimentacao.quantidade, movimentacao.observacoes])
        
        return response
