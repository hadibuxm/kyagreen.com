from django.contrib import admin
from .models import HomePage, InformationPage, ContactInfo


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'hero_image', 'is_active')
        }),
        ('Content', {
            'fields': ('content', 'welcome_section')
        }),
    )


@admin.register(InformationPage)
class InformationPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Page Information', {
            'fields': ('title', 'image')
        }),
        ('Content', {
            'fields': ('content', 'mission', 'vision')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not InformationPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Details', {
            'fields': ('address', 'phone', 'email', 'whatsapp', 'working_hours')
        }),
        ('WeChat', {
            'fields': ('wechat_qr',),
            'description': 'Upload your WeChat QR code image. Customers can scan this from the WeChat icon in the sidebar.'
        }),
        ('Map', {
            'fields': ('map_embed',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
