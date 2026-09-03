from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Supplier, Customer

# Usamos o ImportExportModelAdmin em vez do admin padrão
@admin.register(Supplier)
class SupplierAdmin(ImportExportModelAdmin):
    list_display = ('name','contact','phone','email','cnpj')

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('name','contact','phone','email','cnpj_cpf')