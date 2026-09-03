from django.db import models
from datetime import date

class AccountCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Categoria (Ex: Impostos, Matéria-Prima)")
    
    def __str__(self):
        return self.name

class FinancialRecord(models.Model):
    RECORD_TYPES = [
        ('PAYABLE', 'Conta a Pagar'),
        ('RECEIVABLE', 'Conta a Receber'),
    ]
    STATUS = [
        ('PENDING', 'Pendente'),
        ('PAID', 'Pago/Recebido'),
        ('CANCELED', 'Cancelado'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Descrição")
    record_type = models.CharField(max_length=15, choices=RECORD_TYPES, verbose_name="Tipo")
    category = models.ForeignKey(AccountCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria Contábil")
    
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Total")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    payment_date = models.DateField(null=True, blank=True, verbose_name="Data do Pagamento Realizado")
    
    status = models.CharField(max_length=15, choices=STATUS, default='PENDING', verbose_name="Status de Pagamento")
    delivery_status = models.CharField(max_length=50, default='-', verbose_name="Status de Entrega")
    
    purchase_order = models.ForeignKey('orders.PurchaseOrder', on_delete=models.CASCADE, null=True, blank=True)
    sales_order = models.ForeignKey('orders.SalesOrder', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_record_type_display()} | {self.title} | R$ {self.amount}"