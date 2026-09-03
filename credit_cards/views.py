from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import CreditCard, CreditCardExpense, MonthlyCardDueOverride
from finance.models import FinancialRecord

@staff_member_required
def credit_card_dashboard_view(request, card_id=None):
    cards = CreditCard.objects.all()
    selected_card = get_object_or_404(CreditCard, id=card_id) if card_id else cards.first()
    
    if request.method == 'POST' and selected_card:
        if 'add_expense' in request.POST:
            desc = request.POST.get('description')
            p_date = request.POST.get('purchase_date')
            amount = request.POST.get('total_amount')
            installments = request.POST.get('installments_count', 1)
            
            if desc and p_date and amount:
                CreditCardExpense.objects.create(
                    card=selected_card,
                    description=desc,
                    purchase_date=p_date,
                    total_amount=amount,
                    installments_count=int(installments)
                )
            return redirect('credit_cards:dashboard_card', card_id=selected_card.id)
            
        elif 'update_due' in request.POST:
            mes_ano = request.POST.get('mes_ano')
            new_date_str = request.POST.get('due_date')
            if mes_ano and new_date_str:
                new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
                MonthlyCardDueOverride.objects.update_or_create(
                    card=selected_card,
                    mes_ano=mes_ano,
                    defaults={'due_date': new_date}
                )
            return redirect('credit_cards:dashboard_card', card_id=selected_card.id)

    colunas_meses = []
    linhas_tabela = []
    
    if selected_card:
        hoje = date.today().replace(day=1)
        overrides = {o.mes_ano: o.due_date for o in selected_card.due_overrides.all()}
        
        # Calcula a quantidade de meses até dezembro de 2030 dinamicamente
        data_limite = date(2030, 12, 1)
        diferenca_anos = data_limite.year - hoje.year
        diferenca_meses = data_limite.month - hoje.month
        total_meses = (diferenca_anos * 12) + diferenca_meses + 1
        if total_meses < 12:
            total_meses = 12 # Garante pelo menos 12 meses caso a data atual ultrapasse
        
        for i in range(total_meses):
            m = hoje + relativedelta(months=i)
            mes_key = m.strftime("%B_%Y").lower()
            
            try:
                default_due = m.replace(day=selected_card.due_day)
            except ValueError:
                next_month = m + relativedelta(months=1)
                default_due = next_month - relativedelta(days=1)
                
            due_date = overrides.get(mes_key, default_due)
            
            colunas_meses.append({
                'key': mes_key,
                'mes_ano': mes_key,
                'label': m.strftime("%B / %Y").capitalize(),
                'total': Decimal('0.00'),
                'due_date': due_date
            })
            
        expenses = selected_card.expenses.all().order_by('purchase_date')
        
        for exp in expenses:
            qtd = exp.installments_count if exp.installments_count > 0 else 1
            valor_parcela = (exp.total_amount / Decimal(qtd)).quantize(Decimal('0.01'))
            diferenca = exp.total_amount - (valor_parcela * qtd)
            
            for i in range(qtd):
                curr_valor = valor_parcela
                if i == qtd - 1:
                    curr_valor += diferenca
                    
                target_date = exp.purchase_date + relativedelta(months=i)
                mes_key = target_date.strftime("%B_%Y").lower()
                
                celulas = []
                for col in colunas_meses:
                    val = curr_valor if col['key'] == mes_key else Decimal('0.00')
                    celulas.append({'mes_key': col['key'], 'valor': val})
                    
                    if col['key'] == mes_key:
                        col['total'] += curr_valor

                parcela_str = f"{i+1}/{qtd}" if qtd > 1 else ""
                
                linhas_tabela.append({
                    'purchase_date': exp.purchase_date,
                    'description': exp.description,
                    'parcela_str': parcela_str,
                    'celulas_meses': celulas
                })

        # Sincroniza o total da fatura de cada mês com o FinancialRecord (Fluxo de Caixa)
        for col in colunas_meses:
            if col['total'] > 0:
                record_title = f"Fatura Cartão: {selected_card.name} ({col['label']})"
                FinancialRecord.objects.update_or_create(
                    title=record_title,
                    record_type='PAYABLE',
                    defaults={
                        'amount': col['total'],
                        'due_date': col['due_date'],
                        'status': 'PENDING'
                    }
                )

    context = {
        'cards': cards,
        'selected_card': selected_card,
        'colunas_meses': colunas_meses,
        'linhas_tabela': linhas_tabela,
    }
    return render(request, 'credit_cards/dashboard.html', context)