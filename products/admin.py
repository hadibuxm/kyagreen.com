from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order']


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    fields = ['name', 'value', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price', 'in_stock', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'in_stock', 'category', 'created_at']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'in_stock']
    inlines = [ProductImageInline, ProductAttributeInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'main_image')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'specifications')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'in_stock', 'stock_quantity')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
