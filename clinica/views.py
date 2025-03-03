from django.shortcuts import render, redirect, get_object_or_404
from .models import Lancamento
from datetime import date
from django.db.models import Q
from .forms import LancamentoForm, LancamentosForm
from decimal import Decimal  # Adicione esta linha
from django.shortcuts import render
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F


def home(request):
    filtro_data = request.GET.get('data', None)
    filtro_descricao = request.GET.get('descricao', None)
    # aqui pega o valor do date...
    filtro_mes_entrada = request.GET.get('mes_entrada', None)
    filtro_mes_saida = request.GET.get('mes_saida', None)
    filtro_forma_pagamento = request.GET.get('forma_pagamento', None)
    pagamentos_pendentes = request.GET.get('pagamentos_pendentes', None)

    hoje = date.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    entradas = Lancamento.objects.filter(tipo='entrada')
    saidas = Lancamento.objects.filter(tipo='saida')

    # Aplicação dos filtros
    if filtro_data:
        entradas = entradas.filter(data=filtro_data)
        # Aplica filtro para saídas também
        saidas = saidas.filter(data=filtro_data)

    if filtro_descricao:
        entradas = entradas.filter(
            Q(nome_cliente__icontains=filtro_descricao) |
            Q(tratamento__icontains=filtro_descricao)
        )
        saidas = saidas.filter(
            Q(nome_cliente__icontains=filtro_descricao) |
            Q(tratamento__icontains=filtro_descricao)
        )

    if filtro_mes_entrada:
        try:
            ano, mes = map(int, filtro_mes_entrada.split('-'))
            entradas = entradas.filter(data__month=mes, data__year=ano)
        except ValueError:
            print("Erro ao processar filtro de mês para entradas.")

    if filtro_forma_pagamento:
        entradas = entradas.filter(forma_pagamento=filtro_forma_pagamento)

    if filtro_mes_saida:
        try:
            ano, mes = map(int, filtro_mes_saida.split('-'))
            saidas = saidas.filter(data__month=mes, data__year=ano)
        except ValueError:
            print("Erro ao processar filtro de mês para saídas.")

    # Filtros combinados
    if filtro_mes_entrada and filtro_descricao:
        try:
            mes, ano = map(int, filtro_mes_entrada.split('-'))
            entradas = Lancamento.objects.filter(
                tipo='entrada',
                data__month=mes,
                data__year=ano,
                nome_cliente__icontains=filtro_descricao  # Simplificado para teste
            )
        except ValueError:
            print("Erro ao processar filtro de mês e descrição para entradas.")

    if filtro_mes_entrada:
        print(f"Filtro recebido: {filtro_mes_entrada}")
        try:
            ano, mes = map(int, filtro_mes_entrada.split('-'))
            print(f"Mês: {mes}, Ano: {ano}")  # Adicionado log
            entradas = Lancamento.objects.filter(
                data__month=mes, data__year=ano)
        except ValueError:
            print("Erro ao processar filtro de mês para entradas.")

    if filtro_mes_saida and filtro_descricao:
        try:
            mes, ano = map(int, filtro_mes_saida.split('-'))
            saidas = Lancamento.objects.filter(
                tipo='saida',
                data__month=mes,
                data__year=ano,
                nome_cliente__icontains=filtro_descricao  # Simplificado para teste
            )
        except ValueError:
            print("Erro ao processar filtro de mês e descrição para saídas.")


    # Cálculo dos totais
    # Obtém os parâmetros da URL
    filtro_mes_entrada = request.GET.get('mes_entrada', '')

# Verifica se há um filtro aplicado
    if filtro_mes_entrada:
        try:
           ano_filtrado, mes_filtrado = map(int, filtro_mes_entrada.split('-'))
        except ValueError:
           ano_filtrado, mes_filtrado = None, None
    else:
        ano_filtrado, mes_filtrado = None, None

# Define os filtros corretos
    if ano_filtrado and mes_filtrado:
       entradas_mes = Lancamento.objects.filter(
        tipo='entrada', data__month=mes_filtrado, data__year=ano_filtrado
    )
       saidas_mes = Lancamento.objects.filter(
          tipo='saida', data__month=mes_filtrado, data__year=ano_filtrado
    )
    else:
       entradas_mes = Lancamento.objects.filter(
        tipo='entrada', data__month=mes_atual, data__year=ano_atual
    )
       saidas_mes = Lancamento.objects.filter(
        tipo='saida', data__month=mes_atual, data__year=ano_atual
    )
       
#Pagamentos pendentes
    # filtro para pagamentos pendentes
    if pagamentos_pendentes is not None:  # Se o botão foi pressionado
      entradas = entradas.filter(valor_pago__lt=F('valor_servico'))

# Cálculo dos totais
    total_entradas_mes = sum(l.valor_pago or 0 for l in entradas_mes)
    total_saidas_mes = sum(l.valor_custo or 0 for l in saidas_mes)

 # Paginação das entradas
    paginator_entradas = Paginator(entradas, 10)
    page_number_entradas = request.GET.get('page_entradas')

    if not page_number_entradas:
        page_number_entradas = paginator_entradas.num_pages

    try:
        entradas_paginadas = paginator_entradas.get_page(page_number_entradas)
    except PageNotAnInteger:
        entradas_paginadas = paginator_entradas.get_page(1)
    except EmptyPage:
        entradas_paginadas = paginator_entradas.get_page(
            paginator_entradas.num_pages)

    # Paginação das saídas
    paginator_saidas = Paginator(saidas, 10)
    page_number_saidas = request.GET.get('page_saidas')

    if not page_number_saidas:
        page_number_saidas = paginator_saidas.num_pages

    try:
        saidas_paginadas = paginator_saidas.get_page(page_number_saidas)
    except PageNotAnInteger:
        saidas_paginadas = paginator_saidas.get_page(1)
    except EmptyPage:
        saidas_paginadas = paginator_saidas.get_page(
            paginator_saidas.num_pages)

    contexto = {
    'entradas': entradas_paginadas,
    'saidas': saidas_paginadas,
    'filtro_data': filtro_data,
    'filtro_descricao': filtro_descricao,
    'filtro_mes_entrada': filtro_mes_entrada,
    'filtro_mes_saida': filtro_mes_saida,
    'filtro_forma_pagamento': filtro_forma_pagamento,
    'total_entradas_mes': total_entradas_mes,
    'total_saidas_mes': total_saidas_mes,
    'mes_filtrado': mes_filtrado if mes_filtrado else mes_atual,
    'ano_filtrado': ano_filtrado if ano_filtrado else ano_atual,
    'pagamentos_pendentes':pagamentos_pendentes,
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
    print(type(lancamento.valor_servico), lancamento.valor_servico)
    if request.method == 'POST':
        lancamento.tipo = request.POST.get('tipo')
        lancamento.nome_cliente = request.POST.get('nome_cliente')
        lancamento.tratamento = request.POST.get('tratamento')

        try:
            lancamento.valor_servico = Decimal(
                request.POST.get('valor_servico') or 0)
            lancamento.valor_pago = Decimal(
                request.POST.get('valor_pago') or 0)
            lancamento.valor_custo = Decimal(
                request.POST.get('valor_custo') or 0)
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
    return redirect('home')  # Substitua pela sua URL de lista
