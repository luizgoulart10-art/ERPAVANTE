from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from datetime import date
from .models import PurchaseOrder, SalesOrder
from inventory.models import StockMovement
from finance.models import FinancialRecord

@receiver(post_save, sender=PurchaseOrder)
def process_purchase_completion(sender, instance, **kwargs):
    if instance.status == 'COMPLETED' and not instance.stock_received:
        with transaction.atomic():
            # 1. Dar entrada no estoque
            for item in instance.items.all():
                StockMovement.objects.create(
                    product=item.product, quantity=item.quantity,
                    movement_type='IN', description=f"Entrada Pedido #{instance.id}"
                )
            instance.stock_received = True
            PurchaseOrder.objects.filter(id=instance.id).update(stock_received=True)

            # 2. Gerar Conta a Pagar (se não existir)
            if not FinancialRecord.objects.filter(purchase_order=instance).exists():
                vencimento = instance.receipt_date if instance.receipt_date else date.today()
                FinancialRecord.objects.create(
                    title=f"Pagamento Pedido Compra #{instance.id} - {instance.supplier.name}",
                    record_type='PAYABLE',
                    amount=instance.total_value,
                    due_date=vencimento,
                    purchase_order=instance
                )

@receiver(post_save, sender=SalesOrder)
def process_sale_completion(sender, instance, **kwargs):
    if instance.status == 'COMPLETED' and not instance.stock_deducted:
        with transaction.atomic():
            # 1. Dar baixa no estoque
            for item in instance.items.all():
                StockMovement.objects.create(
                    product=item.product, quantity=item.quantity,
                    movement_type='OUT', description=f"Saída Venda #{instance.id}"
                )
            instance.stock_deducted = True
            SalesOrder.objects.filter(id=instance.id).update(stock_deducted=True)

            # 2. Gerar Conta a Receber (se não existir)
            if not FinancialRecord.objects.filter(sales_order=instance).exists():
                vencimento = instance.delivery_date if instance.delivery_date else date.today()
                FinancialRecord.objects.create(
                    title=f"Recebimento Venda #{instance.id} - {instance.customer.name}",
                    record_type='RECEIVABLE',
                    amount=instance.total_value,
                    due_date=vencimento,
                    sales_order=instance
                )