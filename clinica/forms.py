from django import forms
from .models import Lancamento

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = [
            'tipo',
            'data',
            'nome_cliente',
            'tratamento',
            'valor_servico',
            'valor_pago',
            'forma_pagamento',
            'discriminacao',
            'valor_custo',
        ]
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'discriminacao': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicione classes CSS para ocultar/exibir os campos
        self.fields['nome_cliente'].widget.attrs['class'] = 'entrada-field'
        self.fields['tratamento'].widget.attrs['class'] = 'entrada-field'
        self.fields['valor_servico'].widget.attrs['class'] = 'entrada-field'
        self.fields['valor_pago'].widget.attrs['class'] = 'entrada-field'
        self.fields['forma_pagamento'].widget.attrs['class'] = 'entrada-field'
        self.fields['discriminacao'].widget.attrs['class'] = 'saida-field'
        self.fields['valor_custo'].widget.attrs['class'] = 'saida-field'

class LancamentosForm(forms.ModelForm):
    class Meta:
        model = Lancamento
        fields = '__all__'