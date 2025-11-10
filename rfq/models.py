from django.db import models
from products.models import Product


class RFQRequest(models.Model):
    """Request for Quotation model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('quoted', 'Quoted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Customer Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)

    # Request Details
    subject = models.CharField(max_length=300, blank=True, help_text="Request subject")
    message = models.TextField(help_text="Additional details or requirements")
    quantity = models.IntegerField(default=1, help_text="Quantity needed")

    # Product Reference (optional - can be general RFQ or product-specific)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='rfq_requests')

    # Files
    attachment = models.FileField(upload_to='rfq/attachments/', blank=True, null=True, help_text="Optional attachment (specs, drawings, etc.)")

    # Status and Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "RFQ Request"
        verbose_name_plural = "RFQ Requests"
        ordering = ['-created_at']

    def __str__(self):
        if self.product:
            return f"RFQ #{self.id} - {self.name} - {self.product.name}"
        return f"RFQ #{self.id} - {self.name} - General Inquiry"


class RFQItem(models.Model):
    """Multiple items in a single RFQ"""
    rfq = models.ForeignKey(RFQRequest, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=300, help_text="Product name if not in database")
    quantity = models.IntegerField(default=1)
    specifications = models.TextField(blank=True)

    class Meta:
        verbose_name = "RFQ Item"
        verbose_name_plural = "RFQ Items"

    def __str__(self):
        return f"{self.rfq.id} - {self.product_name or self.product.name}"
