from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import SalesOrder, PurchaseOrder, SalesInstallment, PurchaseInstallment
from .models import FinancialRecord

def processar_financeiro_venda(instance):
    FinancialRecord.objects.filter(sales_order=instance).delete()
    
    parcelas = instance.installments.all()
    cliente_nome = instance.customer.name if hasattr(instance, 'customer') and instance.customer else "Cliente"
    total_pedido = getattr(instance, 'total_value', 0) or 0
    status_entrega_texto = instance.get_status_display()

    if parcelas.exists():
        for p in parcelas:
            p_pago = str(getattr(p, 'payment_status', '')).upper() == 'PAID'
            status_fin = 'PAID' if p_pago else 'PENDING'
            
            FinancialRecord.objects.create(
                sales_order=instance,
                record_type='RECEIVABLE',
                title=f"Venda #{instance.id} (Parc {p.installment_number}) - {cliente_nome}",
                amount=p.amount,
                due_date=p.due_date,
                status=status_fin,
                delivery_status=status_entrega_texto,
                payment_date=p.due_date if status_fin == 'PAID' else None
            )
    else:
        data_vencimento = getattr(instance, 'delivery_date', None) or getattr(instance, 'issue_date', None)
        if data_vencimento:
            FinancialRecord.objects.create(
                sales_order=instance,
                record_type='RECEIVABLE',
                title=f"Venda #{instance.id} - {cliente_nome}",
                amount=total_pedido,
                due_date=data_vencimento,
                status='PENDING',
                delivery_status=status_entrega_texto,
                payment_date=None
            )


def processar_financeiro_compra(instance):
    for item in instance.items.all():
        if item.product and hasattr(item, 'unit_price') and item.unit_price is not None:
            item.product.cost_price = item.unit_price
            item.product.save()

    FinancialRecord.objects.filter(purchase_order=instance).delete()
    
    parcelas = instance.installments.all()
    fornecedor_nome = instance.supplier.name if hasattr(instance, 'supplier') and instance.supplier else "Fornecedor"
    total_pedido = getattr(instance, 'total_value', 0) or 0
    status_entrega_texto = instance.get_status_display()

    if parcelas.exists():
        for p in parcelas:
            p_pago = str(getattr(p, 'payment_status', '')).upper() == 'PAID'
            status_fin = 'PAID' if p_pago else 'PENDING'

            FinancialRecord.objects.create(
                purchase_order=instance,
                record_type='PAYABLE',
                title=f"Compra #{instance.id} (Parc {p.installment_number}) - {fornecedor_nome}",
                amount=p.amount,
                due_date=p.due_date,
                status=status_fin,
                delivery_status=status_entrega_texto,
                payment_date=p.due_date if status_fin == 'PAID' else None
            )
    else:
        data_vencimento = getattr(instance, 'receipt_date', None) or getattr(instance, 'issue_date', None)
        if data_vencimento:
            FinancialRecord.objects.create(
                purchase_order=instance,
                record_type='PAYABLE',
                title=f"Compra #{instance.id} - {fornecedor_nome}",
                amount=total_pedido,
                due_date=data_vencimento,
                status='PENDING',
                delivery_status=status_entrega_texto,
                payment_date=None
            )


@receiver(post_save, sender=SalesOrder)
def sincronizar_financeiro_venda(sender, instance, **kwargs):
    processar_financeiro_venda(instance)


@receiver(post_save, sender=PurchaseOrder)
def sincronizar_financeiro_compra(sender, instance, **kwargs):
    processar_financeiro_compra(instance)


@receiver(post_save, sender=SalesInstallment)
def atualizar_venda_via_parcela(sender, instance, **kwargs):
    if instance.sales_order:
        processar_financeiro_venda(instance.sales_order)


@receiver(post_save, sender=PurchaseInstallment)
def atualizar_compra_via_parcela(sender, instance, **kwargs):
    if instance.purchase_order:
        processar_financeiro_compra(instance.purchase_order)