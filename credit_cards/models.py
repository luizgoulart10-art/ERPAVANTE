from django.db import models

class CreditCard(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Cartão (Ex: Nubank, Visa)")
    limit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Limite Total")
    due_day = models.PositiveIntegerField(default=10, verbose_name="Dia de Vencimento Padrão")
    
    def __str__(self):
        return f"{self.name} (Venc. Dia {self.due_day})"

class CreditCardExpense(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='expenses', verbose_name="Cartão de Crédito")
    description = models.CharField(max_length=200, verbose_name="Descrição / Produto")
    purchase_date = models.DateField(verbose_name="Data da Compra")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Total")
    installments_count = models.PositiveIntegerField(default=1, verbose_name="Quantidade de Parcelas")

    def __str__(self):
        return f"{self.description} - R$ {self.total_amount} ({self.installments_count}x)"

class MonthlyCardDueOverride(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='due_overrides')
    mes_ano = models.CharField(max_length=20) # Ex: "janeiro_2026"
    due_date = models.DateField(verbose_name="Data de Vencimento Específica")

    class Meta:
        unique_together = ('card', 'mes_ano')