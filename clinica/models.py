from django.db import models

class Lancamento(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )
    FORMA_PAGAMENTO_CHOICES = (
        ('dinheiro', 'Dinheiro,'),
        ('pix', 'Pix'),
        ('Crédito', 'Crédito'),
        ('débito', 'Débito'),
        ('outros', 'Outros')
    )

    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    data = models.DateField()
    nome_cliente = models.CharField(max_length=100, blank=True, null=True)
    tratamento = models.CharField(max_length=100, blank=True, null=True)
    valor_servico = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    forma_pagamento = models.CharField(max_length=50, blank=True, null=True, choices=FORMA_PAGAMENTO_CHOICES)
    discriminacao = models.TextField(blank=True, null=True)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.data}"
