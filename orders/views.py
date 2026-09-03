from django.shortcuts import render
from .models import PurchaseOrder, SalesOrder

def open_orders_dashboard(request):
    # Busca compras em aberto e ordena pela data de recebimento (prazo)
    compras_abertas = PurchaseOrder.objects.filter(status='OPEN').order_by('receipt_date')
    
    # Busca vendas em aberto e ordena pela data de entrega (prazo)
    vendas_abertas = SalesOrder.objects.filter(status='OPEN').order_by('delivery_date')

    context = {
        'compras_abertas': compras_abertas,
        'vendas_abertas': vendas_abertas,
    }
    
    return render(request, 'orders/open_orders.html', context)
