from django.db import models
from django.core.validators import MinValueValidator


class Form(models.Model):
    """Dynamic form model"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Form description shown to users")
    slug = models.SlugField(unique=True, help_text="URL-friendly version of the title")
    is_active = models.BooleanField(default=True, help_text="Whether users can access this form")
    allow_multiple_submissions = models.BooleanField(default=True, help_text="Allow same user to submit multiple times")
    
    # Settings
    email_notification = models.EmailField(blank=True, help_text="Email to send form submissions to")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Form"
        verbose_name_plural = "Forms"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FormField(models.Model):
    """Fields that belong to a form"""
    FIELD_TYPE_CHOICES = [
        ('text', 'Text Input'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('textarea', 'Text Area'),
        ('select', 'Dropdown'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio Button'),
        ('date', 'Date'),
        ('phone', 'Phone Number'),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=200, help_text="Label shown to users")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    help_text = models.CharField(max_length=500, blank=True)
    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    
    # For select/radio fields: comma-separated options
    choices = models.TextField(blank=True, help_text="Options separated by commas (for dropdown/radio)")
    
    # Validation
    placeholder = models.CharField(max_length=200, blank=True)
    pattern = models.CharField(max_length=500, blank=True, help_text="Regex pattern for validation")

    class Meta:
        verbose_name = "Form Field"
        verbose_name_plural = "Form Fields"
        ordering = ['form', 'order']
        unique_together = ('form', 'label')

    def __str__(self):
        return f"{self.form.title} - {self.label}"

    def get_choices_list(self):
        """Return choices as list"""
        if self.choices:
            return [choice.strip() for choice in self.choices.split(',')]
        return []


class FormSubmission(models.Model):
    """Store form submissions"""
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, help_text="Browser info")

    class Meta:
        verbose_name = "Form Submission"
        verbose_name_plural = "Form Submissions"
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.form.title} - {self.submitted_at}"


class FormSubmissionData(models.Model):
    """Individual field data from form submission"""
    submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name='data')
    field = models.ForeignKey(FormField, on_delete=models.SET_NULL, null=True)
    field_label = models.CharField(max_length=200)  # Store label in case field is deleted
    value = models.TextField()

    class Meta:
        verbose_name = "Form Submission Data"
        verbose_name_plural = "Form Submission Data"

    def __str__(self):
        return f"{self.field_label}: {self.value[:50]}"
