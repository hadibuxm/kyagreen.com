from django.contrib import admin
from .models import RFQRequest, RFQItem


class RFQItemInline(admin.TabularInline):
    model = RFQItem
    extra = 0
    fields = ['product', 'product_name', 'quantity', 'specifications']


@admin.register(RFQRequest)
class RFQRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'company', 'product', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'company', 'subject']
    list_editable = ['status']
    inlines = [RFQItemInline]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone', 'company', 'address')
        }),
        ('Request Details', {
            'fields': ('subject', 'product', 'quantity', 'message', 'attachment')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # Admins can delete RFQ requests
        return request.user.is_superuser
