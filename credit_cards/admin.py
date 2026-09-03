from django.contrib import admin
from .models import CreditCard, CreditCardExpense

class CreditCardExpenseInline(admin.TabularInline):
    model = CreditCardExpense
    extra = 1

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'limit', 'due_day')
    search_fields = ('name',)
    inlines = [CreditCardExpenseInline]