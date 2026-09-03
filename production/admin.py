from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BillOfMaterial, BoMItem, ProductionOrder

class BoMItemInline(admin.TabularInline):
    model = BoMItem
    extra = 1

@admin.register(BillOfMaterial)
class BillOfMaterialAdmin(admin.ModelAdmin):
    inlines = [BoMItemInline]

admin.site.register(ProductionOrder)