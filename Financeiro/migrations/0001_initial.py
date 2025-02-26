# Generated by Django 5.1.6 on 2025-02-26 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pessoas', '0001_initial'),
        ('companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categorias',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='FormasPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('descricao', models.CharField(max_length=25, verbose_name='Tipo de Pagamento')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
                'db_table': 'formaspagamento',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ContaAPagar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('documento', models.CharField(max_length=20, verbose_name='Documento')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('parcela', models.IntegerField(verbose_name='Parcelas')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('data_emissao', models.DateField(verbose_name='Data de Emissão')),
                ('data_vencimento', models.DateField(verbose_name='Vencimento')),
                ('data_pagamento', models.DateField(blank=True, null=True, verbose_name='Data de Pagamento')),
                ('status_pagamento', models.BooleanField(default=False, verbose_name='Status de Pagamento')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('categorias', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.PROTECT, to='Financeiro.categorias')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
                ('pessoas', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contas_a_pagar', to='Pessoas.pessoas')),
                ('forma_pagamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Financeiro.formaspagamento')),
            ],
            options={
                'verbose_name': 'Conta a Pagar',
                'verbose_name_plural': 'Contas a Pagar',
                'db_table': 'contaapagar',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='FormasRecebimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('descricao', models.CharField(max_length=25, verbose_name='Tipo de Recebimento')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Forma de Recebimento',
                'verbose_name_plural': 'Formas de Recebimento',
                'db_table': 'formasrecebimento',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ContaAReceber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('documento', models.CharField(max_length=20, verbose_name='Documento')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('parcela', models.IntegerField(verbose_name='Parcelas')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('data_emissao', models.DateField(verbose_name='Data de Emissão')),
                ('data_vencimento', models.DateField(verbose_name='Vencimento')),
                ('data_recebimento', models.DateField(blank=True, null=True, verbose_name='Data de Recebimento')),
                ('status_recebimento', models.BooleanField(default=False)),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('categorias', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.PROTECT, to='Financeiro.categorias')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
                ('pessoas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas_a_receber', to='Pessoas.pessoas')),
                ('forma_recebimento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Financeiro.formasrecebimento')),
            ],
            options={
                'verbose_name': 'Conta a Receber',
                'verbose_name_plural': 'Contas a Receber',
                'db_table': 'contaareceber',
                'ordering': ['criado', 'id'],
            },
        ),
        migrations.CreateModel(
            name='GerarParcela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vencimento_inicial', models.DateField()),
                ('tipo', models.CharField(choices=[('pagar', 'Pagar'), ('receber', 'Receber')], max_length=10)),
                ('documento', models.PositiveIntegerField(verbose_name='Nº do documento')),
                ('total_parcelas', models.PositiveIntegerField()),
                ('descricao', models.CharField(blank=True, max_length=255, null=True)),
                ('pagamento_total', models.BooleanField(default=False)),
                ('pagamento_parcial', models.BooleanField(default=False)),
                ('valor_pago', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
                ('quitacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Financeiro.formasrecebimento')),
                ('responsavel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gerarparcela', to='Pessoas.pessoas')),
            ],
            options={
                'verbose_name': 'Gerar Parcela',
                'verbose_name_plural': 'Gerar Parcelas',
                'db_table': 'gerarparcelas',
                'ordering': ['criado', 'id'],
            },
        ),
    ]
