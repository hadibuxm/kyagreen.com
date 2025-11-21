from django import forms
from django.forms import Form as DjangoForm
from .models import FormField, FormSubmission, FormSubmissionData


def create_dynamic_form(form_obj):
    """
    Dynamically create a Django form from our Form model
    """
    form_fields = {}
    
    for field in form_obj.fields.all().order_by('order'):
        widget_attrs = {
            'class': 'form-control',
            'placeholder': field.placeholder or field.label,
        }
        
        if field.field_type == 'text':
            form_fields[field.label] = forms.CharField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                widget=forms.TextInput(attrs=widget_attrs)
            )
        
        elif field.field_type == 'email':
            form_fields[field.label] = forms.EmailField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                widget=forms.EmailInput(attrs=widget_attrs)
            )
        
        elif field.field_type == 'number':
            form_fields[field.label] = forms.IntegerField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                widget=forms.NumberInput(attrs=widget_attrs)
            )
        
        elif field.field_type == 'textarea':
            widget_attrs['rows'] = '4'
            form_fields[field.label] = forms.CharField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                widget=forms.Textarea(attrs=widget_attrs)
            )
        
        elif field.field_type == 'select':
            choices = [(choice, choice) for choice in field.get_choices_list()]
            widget_attrs.pop('placeholder', None)
            form_fields[field.label] = forms.ChoiceField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                choices=choices,
                widget=forms.Select(attrs=widget_attrs)
            )
        
        elif field.field_type == 'radio':
            choices = [(choice, choice) for choice in field.get_choices_list()]
            form_fields[field.label] = forms.ChoiceField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                choices=choices,
                widget=forms.RadioSelect(attrs=widget_attrs)
            )
        
        elif field.field_type == 'checkbox':
            widget_attrs.pop('placeholder', None)
            form_fields[field.label] = forms.BooleanField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                widget=forms.CheckboxInput(attrs=widget_attrs)
            )
        
        elif field.field_type == 'date':
            widget_attrs.pop('placeholder', None)
            form_fields[field.label] = forms.DateField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                widget=forms.DateInput(attrs={**widget_attrs, 'type': 'date'})
            )
        
        elif field.field_type == 'phone':
            form_fields[field.label] = forms.CharField(
                label=field.label,
                required=field.is_required,
                help_text=field.help_text,
                widget=forms.TextInput(attrs={**widget_attrs, 'type': 'tel'})
            )
    
    # Create form class dynamically
    DynamicForm = type('DynamicForm', (DjangoForm,), form_fields)
    return DynamicForm
