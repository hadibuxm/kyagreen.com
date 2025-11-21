from django.contrib import admin
from .models import Form, FormField, FormSubmission, FormSubmissionData


class FormFieldInline(admin.TabularInline):
    """Inline admin for form fields"""
    model = FormField
    extra = 1
    fields = ('label', 'field_type', 'is_required', 'order', 'help_text', 'choices', 'placeholder')
    ordering = ('order',)


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """Admin interface for dynamic forms"""
    list_display = ('title', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [FormFieldInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Settings', {
            'fields': ('is_active', 'allow_multiple_submissions', 'email_notification')
        }),
    )


class FormSubmissionDataInline(admin.TabularInline):
    """Inline display of submission data"""
    model = FormSubmissionData
    extra = 0
    readonly_fields = ('field_label', 'value')
    can_delete = False


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    """Admin interface to view form submissions"""
    list_display = ('form', 'submitted_at', 'user_ip')
    list_filter = ('form', 'submitted_at')
    search_fields = ('form__title', 'user_ip')
    readonly_fields = ('form', 'submitted_at', 'user_ip', 'user_agent')
    inlines = [FormSubmissionDataInline]
    
    def has_add_permission(self, request):
        """Prevent manual addition of submissions"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Allow deletion of submissions"""
        return True
