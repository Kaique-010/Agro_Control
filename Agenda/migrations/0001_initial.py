# Generated by Django 5.1.6 on 2025-03-04 23:02

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
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criado em')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('horario', models.TimeField()),
                ('local', models.CharField(blank=True, max_length=200, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.enterprise')),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Pessoas.pessoas')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'db_table': 'evento',
                'ordering': ['id'],
            },
        ),
    ]
