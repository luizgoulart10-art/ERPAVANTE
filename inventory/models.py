from django.db import models
from core.models import Supplier

class Product(models.Model):
    PRODUCT_TYPES = [('RAW', 'Matéria-Prima'), ('FIN', 'Produto Acabado')]
    
    name = models.CharField(max_length=200, verbose_name="Nome do Produto")
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo")
    supplier = models.ForeignKey('core.Supplier', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fornecedor")
    
    # Preço unitário de custo (atualizado automaticamente pelas compras)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Preço Unitário (Custo)")
    
    # Preço de venda opcional (para itens que são comercializados isoladamente)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Preço de Venda (Opcional)")
    
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Quantidade em Estoque")
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Ponto de Reposição")

    def __str__(self):
        return self.name

# NOVA TABELA ADICIONADA AQUI:
class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Entrada (Compra)'),
        ('OUT', 'Saída (Venda)'),
        ('PROD_IN', 'Entrada (Produção)'),
        ('PROD_OUT', 'Consumo (Produção)'),
        ('ADJ', 'Ajuste de Inventário'),
    ]
    
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='movements')
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    movement_type = models.CharField(max_length=15, choices=MOVEMENT_TYPES)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 1. Verifica se é um registro NOVO
        is_new = self.pk is None
        
        # 2. Inteligência: se for Saída ou Consumo, garante que o número seja negativo
        if self.movement_type in ['OUT', 'PROD_OUT'] and self.quantity > 0:
            self.quantity = -self.quantity
            
        # 3. Salva o histórico no banco de dados
        super().save(*args, **kwargs)
        
        # 4. Atualiza o saldo do Produto APENAS se for um movimento novo
        if is_new:
            self.product.stock_quantity += self.quantity
            self.product.save()

    def __str__(self):
        return f"{self.product.name} | {self.quantity} | {self.get_movement_type_display()}"