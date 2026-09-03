from django.contrib import admin
from .models import AccountCategory, FinancialRecord

admin.site.register(AccountCategory)

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'record_type', 'amount', 'due_date', 'status', 'indicador_atraso')
    list_filter = ('record_type', 'status', 'category')
    search_fields = ('title',)
    
    # Trava os campos que vieram de pedidos para evitar fraudes/erros manuais
    readonly_fields = ('purchase_order', 'sales_order')

    @admin.display(description='Atraso?')
    def indicador_atraso(self, obj):
        from datetime import date
        if obj.status == 'PENDING' and obj.due_date < date.today():
            return "🔴 Atrasado"
        elif obj.status == 'PAID':
            return "✅ Ok"
        return "🟡 No prazo"