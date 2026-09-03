from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import ProductionOrder
from inventory.models import StockMovement # <-- Importe a nova tabela aqui

@receiver(post_save, sender=ProductionOrder)
def update_stock_on_production(sender, instance, created, **kwargs):
    if instance.status == 'DONE':
        with transaction.atomic():
            # 1. Dar baixa na matéria-prima
            for item in instance.bom.items.all():
                material = item.raw_material
                qtd_consumida = item.quantity * instance.quantity_to_produce
                
                # Atualiza o saldo
                material.stock_quantity -= qtd_consumida
                material.save()
                
                # Salva no histórico de inventário
                StockMovement.objects.create(
                    product=material,
                    quantity=-qtd_consumida, # Negativo porque é saída
                    movement_type='PROD_OUT',
                    description=f"Consumo OP #{instance.id}"
                )
            
            # 2. Dar entrada no produto acabado
            finished = instance.bom.finished_product
            
            # Atualiza o saldo
            finished.stock_quantity += instance.quantity_to_produce
            finished.save()
            
            # Salva no histórico de inventário
            StockMovement.objects.create(
                product=finished,
                quantity=instance.quantity_to_produce, # Positivo porque é entrada
                movement_type='PROD_IN',
                description=f"Produção OP #{instance.id}"
            )