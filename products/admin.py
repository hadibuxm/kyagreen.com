from django import forms
from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute


class ProductAdminForm(forms.ModelForm):
    """Custom form to display categories hierarchically"""
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(),
        required=False,
        help_text="Select a category for this product"
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get all categories and sort them by hierarchy
        categories = Category.objects.all().order_by('order', 'name')
        
        # Create a sorted queryset with hierarchical display
        choices = [('', '---------')]  # Empty choice
        
        def add_category_choices(category, level=0):
            """Recursively add categories with indentation"""
            indent = '  ' * level  # Use spaces for indentation
            display_name = f"{indent}{'└─ ' if level > 0 else ''}{category.name}"
            choices.append((category.id, display_name))
            
            # Add children
            for child in category.children.all().order_by('order', 'name'):
                add_category_choices(child, level + 1)
        
        # Add root categories first
        root_categories = categories.filter(parent__isnull=True)
        for cat in root_categories:
            add_category_choices(cat)
        
        self.fields['category'].choices = choices


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
    form = ProductAdminForm
    list_display = ['name', 'sku', 'category', 'price', 'in_stock', 'is_active', 'is_featured', 'created_at']
    list_filter = ['is_active', 'is_featured', 'in_stock', 'category', 'created_at']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_featured', 'in_stock']
    inlines = [ProductImageInline, ProductAttributeInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'company', 'main_image')
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
