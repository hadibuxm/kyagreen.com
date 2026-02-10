from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Product categories with hierarchical support"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        help_text="Recommended: 300x300px (Square 1:1), JPEG/WebP, under 100KB"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.get_hierarchical_name()

    def get_hierarchical_name(self):
        """Return category name with hierarchy indentation"""
        if self.parent:
            parent_name = self.parent.get_hierarchical_name()
            return f"{parent_name} → {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Product model with all details"""
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, help_text="Stock Keeping Unit")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    company = models.CharField(max_length=200, blank=True, help_text="Company or manufacturer name")
    short_description = models.TextField(max_length=500, blank=True)
    description = RichTextField()
    specifications = RichTextField(blank=True, help_text="Technical specifications")

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Display price (optional)")

    # Images
    main_image = models.ImageField(
        upload_to='products/',
        help_text="Recommended: 800x800 to 1200x1200px (Square 1:1), JPEG/WebP, under 500KB"
    )

    # Inventory
    in_stock = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0, help_text="Available quantity")

    # Meta
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Additional product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='products/gallery/',
        help_text="Recommended: 800x800 to 1200x1200px (Square 1:1), JPEG/WebP, under 500KB"
    )
    alt_text = models.CharField(max_length=200, blank=True, help_text="Descriptive text for accessibility")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class ProductAttribute(models.Model):
    """Custom attributes for products (e.g., Color, Size, Material)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
