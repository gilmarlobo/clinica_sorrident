# Generated by Django 5.1.6 on 2025-02-26 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0002_lancamento_tratamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lancamento',
            name='forma_pagamento',
            field=models.CharField(blank=True, choices=[('dinheiro', 'Dinheiro,'), ('pix', 'Pix'), ('Crédito', 'Crédito'), ('débito', 'Débito'), ('outros', 'Outros')], max_length=50, null=True),
        ),
    ]
