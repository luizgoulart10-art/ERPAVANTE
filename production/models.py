from django.db import models

# Create your models here.
from django.db import models
from inventory.models import Product

class BillOfMaterial(models.Model):
    finished_product = models.OneToOneField(
        Product, on_delete=models.CASCADE, 
        limit_choices_to={'type': 'FIN'}
    )

    def __str__(self):
        return f"BoM: {self.finished_product.name}"

class BoMItem(models.Model):
    bom = models.ForeignKey(BillOfMaterial, related_name='items', on_delete=models.CASCADE)
    raw_material = models.ForeignKey(
        Product, on_delete=models.RESTRICT, 
        limit_choices_to={'type': 'RAW'}
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=4)

class ProductionOrder(models.Model):
    STATUS = [('PENDING', 'Pendente'), ('DONE', 'Concluído')]
    
    bom = models.ForeignKey(BillOfMaterial, on_delete=models.RESTRICT)
    quantity_to_produce = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default='PENDING')