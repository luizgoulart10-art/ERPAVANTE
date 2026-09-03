from django.contrib import admin
from .models import (
    SalesOrder, SalesOrderItem, SalesInstallment,
    PurchaseOrder, PurchaseOrderItem, PurchaseInstallment
)
from finance.signals import processar_financeiro_venda, processar_financeiro_compra

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1

class SalesInstallmentInline(admin.TabularInline):
    model = SalesInstallment
    extra = 1

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1

class PurchaseInstallmentInline(admin.TabularInline):
    model = PurchaseInstallment
    extra = 1

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'resumo_itens', 'issue_date', 'delivery_date', 'total_value')
    list_filter = ('status', 'customer')
    readonly_fields = ('total_value',) 
    inlines = [SalesOrderItemInline, SalesInstallmentInline]

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        processar_financeiro_venda(form.instance)

    @admin.display(description='Produtos (Qtd)')
    def resumo_itens(self, obj):
        itens = obj.items.all()
        if not itens:
            return "Sem itens"
        lista_produtos = [f"{item.product.name} ({int(item.quantity)})" for item in itens]
        texto = ", ".join(lista_produtos)
        return texto[:60] + "..." if len(texto) > 60 else texto


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'status', 'resumo_itens', 'issue_date', 'total_value')
    list_filter = ('status', 'supplier')
    readonly_fields = ('total_value',) 
    inlines = [PurchaseOrderItemInline, PurchaseInstallmentInline]

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)
        processar_financeiro_compra(form.instance)

    @admin.display(description='Itens (Qtd)')
    def resumo_itens(self, obj):
        itens = obj.items.all()
        if not itens:
            return "Sem itens"
        lista_produtos = [f"{item.product.name} ({int(item.quantity)})" for item in itens]
        texto = ", ".join(lista_produtos)
        return texto[:60] + "..." if len(texto) > 60 else texto