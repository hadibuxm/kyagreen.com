from django import forms
from .models import RFQRequest


class RFQRequestForm(forms.ModelForm):
    class Meta:
        model = RFQRequest
        fields = ['name', 'email', 'phone', 'company', 'address', 'subject',
                  'product', 'quantity', 'message', 'attachment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name (Optional)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your Address (Optional)'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject of your request'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Please provide details about your requirements...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'company': 'Company Name',
            'address': 'Address',
            'subject': 'Subject',
            'product': 'Product (Optional - select if specific product)',
            'quantity': 'Quantity Required',
            'message': 'Message / Requirements',
            'attachment': 'Attachment (Optional)',
        }

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)
        super().__init__(*args, **kwargs)

        # Make product field not required (for general RFQ)
        self.fields['product'].required = False

        # If product_id is provided, set it as initial value
        if product_id:
            self.initial['product'] = product_id
