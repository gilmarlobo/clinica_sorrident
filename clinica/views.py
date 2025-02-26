from django.shortcuts import render, redirect, get_object_or_404
from .models import Lancamento
from datetime import date
from django.db.models import Q
from .forms import LancamentoForm, LancamentosForm
from decimal import Decimal  # Adicione esta linha

from django.shortcuts import render
from datetime import date


def home(request):
    filtro_data = request.GET.get('data', None)
    filtro_descricao = request.GET.get('descricao', None)
    filtro_mes_entrada = request.GET.get(
        'mes_entrada', None)  # Filtro de mês para entradas
    filtro_mes_saida = request.GET.get(
        'mes_saida', None)  # Filtro de mês para saídas
    filtro_forma_pagamento = request.GET.get('forma_pagamento', None)

    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    entradas = Lancamento.objects.filter(tipo='entrada')
    saidas = Lancamento.objects.filter(tipo='saida')

    # Filtros para entradas
    if filtro_data:
        entradas = entradas.filter(data=filtro_data)

    if filtro_descricao:
        entradas = entradas.filter(
            Q(nome_cliente__icontains=filtro_descricao) |
            Q(tratamento__icontains=filtro_descricao)
        )

    if filtro_mes_entrada:
        mes, ano = filtro_mes_entrada.split('-')
        entradas = entradas.filter(data__month=int(mes), data__year=int(ano))

    if filtro_forma_pagamento:
        entradas = entradas.filter(forma_pagamento=filtro_forma_pagamento)

    if filtro_mes_saida:
        print(f"Filtro de mês para saídas recebido: {filtro_mes_saida}")
        if saidas.exists():  # Verifica se há saídas antes de filtrar
            try:
                mes, ano = filtro_mes_saida.split('-')
                if mes.isdigit() and ano.isdigit():
                    print(f"Mês: {mes}, Ano: {ano}")
                    saidas = saidas.filter(
                        data__month=int(mes), data__year=int(ano))
                    print(f"Saídas encontradas: {saidas}")
                else:
                    print("Erro: Mês ou ano não são numéricos.")
            except ValueError:
                print("Erro ao processar o filtro de mês para saídas.")
        else:
            print("Atenção: Não há saídas para filtrar.")
    # Cálculo dos totais de entradas e saídas do mês corrente
    entradas_mes = Lancamento.objects.filter(
        tipo='entrada',
        data__month=mes_atual,
        data__year=ano_atual
    )
    saidas_mes = Lancamento.objects.filter(
        tipo='saida',
        data__month=mes_atual,
        data__year=ano_atual
    )

    total_entradas_mes = sum(
        lancamento.valor_pago or 0 for lancamento in entradas_mes)
    total_saidas_mes = sum(
        lancamento.valor_custo or 0 for lancamento in saidas_mes)

    contexto = {
        'entradas': entradas,
        'saidas': saidas,
        'filtro_data': filtro_data,
        'filtro_descricao': filtro_descricao,
        'filtro_mes_entrada': filtro_mes_entrada,
        'filtro_mes_saida': filtro_mes_saida,
        'filtro_forma_pagamento': filtro_forma_pagamento,
        'total_entradas_mes': total_entradas_mes,
        'total_saidas_mes': total_saidas_mes,
    }

    return render(request, 'clinica/home.html', contexto)


def registrar(request):
    data = request.GET.get('data', None)
    print(data)

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        if tipo == 'entrada':
            Lancamento.objects.create(
                tipo=tipo,
                data=data,  # Use a data da URL
                nome_cliente=request.POST.get('nome_cliente'),
                tratamento=request.POST.get('tratamento'),
                valor_servico=request.POST.get('valor_servico'),
                valor_pago=request.POST.get('valor_pago'),
                forma_pagamento=request.POST.get('forma_pagamento')
            )
        elif tipo == 'saida':
            Lancamento.objects.create(
                tipo=tipo,
                data=data,  # Use a data da URL
                discriminacao=request.POST.get('discriminacao'),
                valor_custo=request.POST.get('valor_custo')
            )
        return redirect('home')

    return render(request, 'clinica/registrar.html', {'data': data})

def editar_registro(request, registro_id):
    lancamento = get_object_or_404(Lancamento, id=registro_id)

    if request.method == 'POST':
        lancamento.tipo = request.POST.get('tipo')
        lancamento.nome_cliente = request.POST.get('nome_cliente')
        lancamento.tratamento = request.POST.get('tratamento')

        try:
            lancamento.valor_servico = Decimal(request.POST.get('valor_servico') or 0)
            lancamento.valor_pago = Decimal(request.POST.get('valor_pago') or 0)
            lancamento.valor_custo = Decimal(request.POST.get('valor_custo') or 0)
        except (ValueError, TypeError):
            # Lidar com erro de conversão (por exemplo, exibir uma mensagem de erro)
            return render(request, 'clinica/registrar.html', {'lancamento': lancamento, 'error': 'Valores numéricos inválidos'})

        lancamento.forma_pagamento = request.POST.get('forma_pagamento')
        lancamento.discriminacao = request.POST.get('discriminacao')
        lancamento.save()
        return redirect('home')

    return render(request, 'clinica/registrar.html', {'lancamento': lancamento})

def apagar_registro(request, registro_id):
    registro = get_object_or_404(Lancamento, id=registro_id)
    registro.delete()
    return redirect('home') # Substitua pela sua URL de lista