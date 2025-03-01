# Generated by Django 5.1.6 on 2025-02-28 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Financeiro', '0005_alter_centrodecusto_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centrodecusto',
            name='tipo',
            field=models.CharField(choices=[('debito', 'Débito'), ('credito', 'Crédito'), ('projetos', 'Projetos'), ('extras', 'Extras')], max_length=10),
        ),
        migrations.CreateModel(
            name='PlanoDeContas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('codigo', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('tipo', models.CharField(choices=[('ativos', 'Ativos'), ('passivos', 'Passivos'), ('receitas', 'Receitas'), ('despesas', 'Despesas')], max_length=10)),
                ('movimento', models.CharField(choices=[('debito', 'Débito'), ('credito', 'Crédito')], default='debito', max_length=7)),
                ('resumido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expandido', to='Financeiro.planodecontas')),
            ],
            options={
                'verbose_name': 'Plano de Contas',
                'verbose_name_plural': 'Planos de Contas',
                'db_table': 'planodecontas',
                'ordering': ['codigo'],
            },
        ),
    ]
