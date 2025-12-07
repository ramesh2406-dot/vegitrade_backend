from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_kg', 'stock_kg', 'supplier_name')
    search_fields = ('name', 'supplier_name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'product', 'quantity_kg', 'total_price', 'status')
    list_filter = ('status', 'created_at')
