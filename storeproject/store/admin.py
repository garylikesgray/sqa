from django.contrib import admin
from .models import Category, Product, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'total_price', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'name', 'email', 'address', 'total_price', 'created_at']
