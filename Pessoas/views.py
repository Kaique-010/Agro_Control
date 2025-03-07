from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
import openpyxl
import requests
from . import models, forms
from django.urls import reverse_lazy
from django.db import IntegrityError, connections
from django.core.exceptions import ObjectDoesNotExist


        

class PessoasListView( ListView):
    model = models.Pessoas
    template_name = 'pessoaslistas.html'
    context_object_name = 'pessoas'
    paginate_by = 10

    def get_queryset(self):
       
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')
        
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        
        return queryset
   
    def form_valid(self, form):
        # Aqui, o usuário logado é passado para o formulário
        form.save(user=self.request.user)
        return super().form_valid(form)
    
    


class PessoasCreateView(CreateView):
    model = models.Pessoas
    template_name = 'pessoascriar.html'
    form_class = forms.Pessoas
    success_url = reverse_lazy('pessoaslistas')

    def form_valid(self, form):
        
        self.object = form.save(user=self.request.user)
        cep = form.cleaned_data.get('cep')
        dados_endereco = buscar_cep(cep)

        if dados_endereco and 'erro' not in dados_endereco:
            form.instance.logradouro = dados_endereco.get('logradouro')
            form.instance.bairro = dados_endereco.get('bairro')
            form.instance.cidade = dados_endereco.get('localidade')
            form.instance.estado = dados_endereco.get('uf')
            
        return super().form_valid(form)


class PessoasDetailView(DetailView):
    model = models.Pessoas
    template_name = 'pessoasdetalhe.html'

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        

        
        queryset = self.model.objects.all()
        return super().get_object(queryset=queryset)

class PessoasUpdateView(UpdateView):
    model = models.Pessoas
    template_name = 'pessoaseditar.html'
    form_class = forms.Pessoas
    success_url = reverse_lazy('pessoaslistas')

    def form_valid(self, form):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
       
        
        cep = form.cleaned_data.get('cep')
        dados_endereco = buscar_cep(cep)
        if dados_endereco and 'erro' not in dados_endereco:
            form.instance.logradouro = dados_endereco.get('logradouro')
            form.instance.bairro = dados_endereco.get('bairro')
            form.instance.cidade = dados_endereco.get('localidade')
            form.instance.estado = dados_endereco.get('uf')
        
        return super().form_valid(form)

class PessoasDeleteView(DeleteView):
    model = models.Pessoas
    template_name = 'pessoasexcluir.html'
    success_url = reverse_lazy('pessoaslistas')

    def get_object(self):
        if not self.request.user.empresa:
            raise IntegrityError("Usuário não associado a uma empresa")
        
       
        
        queryset = self.model.objects.all()
        return super().get_object(queryset=queryset)

def exportar_pessoas_excel(request):
    if not request.user.empresa:
        raise IntegrityError("Usuário não associado a uma empresa")
    

    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Pessoas'

    # Define o cabeçalho
    columns = ['ID', 'Nome', 'RG', 'CPF', 'CNPJ', 'IE', 'Telefone', 'Classificação']
    worksheet.append(columns)

    # Adiciona os dados
    pessoas = models.Pessoas.objects.all()  
    for pessoa in pessoas:
        worksheet.append([
            pessoa.id,
            pessoa.nome,
            pessoa.rg,
            pessoa.cpf,
            pessoa.cnpj,
            pessoa.ie,
            pessoa.telefone,
            pessoa.classificacao,
        ])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=pessoas.xlsx'
    return response


def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None



