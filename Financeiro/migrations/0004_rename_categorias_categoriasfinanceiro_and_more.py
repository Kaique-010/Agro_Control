# Generated by Django 5.1.6 on 2025-02-26 23:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Financeiro', '0003_centrodecusto_filho'),
        ('companies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categorias',
            new_name='CategoriasFinanceiro',
        ),
        migrations.AlterModelTable(
            name='categoriasfinanceiro',
            table='categoriasfinanceiro',
        ),
    ]
