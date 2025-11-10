from django.contrib import admin
from .models import Service, ServiceFeature


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ['title', 'description', 'order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active', 'order']
    inlines = [ServiceFeatureInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'icon', 'image', 'order')
        }),
        ('Content', {
            'fields': ('short_description', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
