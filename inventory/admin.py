from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, StockMovement

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    # Define as colunas que vão aparecer na lista
    list_display = (
        'name', 
        'type', 
        'stock_quantity', 
        'cost_price_formatted', 
        'valor_total_estoque', 
        'reorder_point', 
        'status_estoque'
    )
    
    # Adiciona filtros laterais
    list_filter = ('type', 'supplier')
    
    # Cria uma barra de pesquisa por nome do produto
    search_fields = ('name',)
    
    # Apenas o saldo em estoque continua travado (para forçar o uso de movimentações)
    readonly_fields = ('stock_quantity',)

    # Função personalizada para formatar o Valor Unitário (Custo)
    @admin.display(description='Valor Unitário')
    def cost_price_formatted(self, obj):
        preco = getattr(obj, 'cost_price', 0) or 0
        return f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Função personalizada para calcular o Valor Total (Quantidade x Preço Unitário)
    @admin.display(description='Valor Total')
    def valor_total_estoque(self, obj):
        quantidade = getattr(obj, 'stock_quantity', 0) or 0
        preco = getattr(obj, 'cost_price', 0) or 0
        total = quantidade * preco
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Função personalizada para criar uma coluna de "Status"
    @admin.display(description='Status')
    def status_estoque(self, obj):
        if obj.stock_quantity <= 0:
            return "❌ Sem Estoque"
        elif obj.stock_quantity <= obj.reorder_point:
            return "⚠️ Pedir Reposição"
        return "✅ OK"


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    # Configura as colunas que vão aparecer na lista do painel
    list_display = ('product', 'quantity', 'movement_type', 'created_at')
    # Cria um filtro lateral para buscar rápido
    list_filter = ('movement_type', 'product', 'created_at')