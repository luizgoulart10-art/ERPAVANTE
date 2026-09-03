from django.shortcuts import render
from django.db.models import Sum
from .models import FinancialRecord

def cash_flow_dashboard(request):
    # 1. Realizado (O que já foi Pago/Recebido de fato)
    entradas_real = FinancialRecord.objects.filter(record_type='RECEIVABLE', status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    saidas_real = FinancialRecord.objects.filter(record_type='PAYABLE', status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
    saldo_real = entradas_real - saidas_real

    # 2. Pendentes (A Pagar / A Receber)
    entradas_pend = FinancialRecord.objects.filter(record_type='RECEIVABLE', status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
    saidas_pend = FinancialRecord.objects.filter(record_type='PAYABLE', status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 3. Saldo Projetado (Caixa atual + O que vai entrar - O que vai sair)
    saldo_projetado = saldo_real + entradas_pend - saidas_pend

    # 4. EXTRATO: Buscar todos os registros ordenados por data de vencimento
    registros = FinancialRecord.objects.all().order_by('due_date')

    context = {
        'entradas_real': entradas_real,
        'saidas_real': saidas_real,
        'saldo_real': saldo_real,
        'entradas_pend': entradas_pend,
        'saidas_pend': saidas_pend,
        'saldo_projetado': saldo_projetado,
        'registros': registros, # Enviando a lista para a tela
    }
    
    return render(request, 'finance/cash_flow.html', context)