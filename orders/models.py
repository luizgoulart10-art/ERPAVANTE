from django.db import models
from core.models import Supplier, Customer
from inventory.models import Product

class PurchaseOrder(models.Model):
    STATUS = [
        ('NEEDED', 'Necessário (Sugestão)'),
        ('OPEN', 'Em Aberto (Aguardando Entrega)'),
        ('COMPLETED', 'Concluído (Recebido)'),
        ('CANCELED', 'Cancelado'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT, verbose_name="Fornecedor")
    status = models.CharField(max_length=20, choices=STATUS, default='NEEDED', verbose_name="Status de Entrega/Pedido")
    
    issue_date = models.DateField(null=True, blank=True, verbose_name="Data de Colocação")
    receipt_date = models.DateField(null=True, blank=True, verbose_name="Data de Recebimento")
    
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valor Total")
    notes = models.TextField(blank=True, verbose_name="Observações")
    stock_received = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.supplier.name}"

class PurchaseOrderItem(models.Model):
    order = models.ForeignKey(PurchaseOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        total = sum(item.total_price for item in self.order.items.all())
        PurchaseOrder.objects.filter(id=self.order.id).update(total_value=total)


class SalesOrder(models.Model):
    STATUS = [
        ('QUOTATION', 'Orçamento'),
        ('OPEN', 'Em Aberto (Aguardando Envio)'),
        ('COMPLETED', 'Concluído (Entregue)'),
        ('CANCELED', 'Cancelado'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Cliente")
    status = models.CharField(max_length=20, choices=STATUS, default='QUOTATION', verbose_name="Status de Entrega/Pedido")
    
    issue_date = models.DateField(auto_now_add=True, verbose_name="Data de Emissão")
    delivery_date = models.DateField(null=True, blank=True, verbose_name="Data de Entrega")
    
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valor Total")
    notes = models.TextField(blank=True, verbose_name="Observações")
    stock_deducted = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"Venda #{self.id} - {self.customer.name}"

class SalesOrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantidade")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        
        total = sum(item.total_price for item in self.order.items.all())
        SalesOrder.objects.filter(id=self.order.id).update(total_value=total)


class SalesInstallment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Realizado / Pago'),
        ('OVERDUE', 'Atrasado'),
        ('CANCELED', 'Cancelado'),
    ]

    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='installments', verbose_name="Pedido de Venda")
    installment_number = models.PositiveIntegerField(verbose_name="Número da Parcela")
    due_date = models.DateField(verbose_name="Data de Recebimento")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Parcela")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING', verbose_name="Status de Pagamento")

    def __str__(self):
        return f"Parcela {self.installment_number} - R$ {self.amount} ({self.get_payment_status_display()})"


class PurchaseInstallment(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Realizado / Pago'),
        ('OVERDUE', 'Atrasado'),
        ('CANCELED', 'Cancelado'),
    ]

    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='installments', verbose_name="Pedido de Compra")
    installment_number = models.PositiveIntegerField(verbose_name="Número da Parcela")
    due_date = models.DateField(verbose_name="Data de Pagamento")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Parcela")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING', verbose_name="Status de Pagamento")

    def __str__(self):
        return f"Parcela {self.installment_number} - R$ {self.amount} ({self.get_payment_status_display()})"