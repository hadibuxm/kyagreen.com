from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils.decorators import decorator_from_middleware_with_args
from django.middleware.common import CommonMiddleware
from .models import Form, FormSubmission, FormSubmissionData, FormField
from .forms import create_dynamic_form


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def form_list(request):
    """Display all active forms"""
    forms = Form.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'forms': forms,
        'page_title': 'All Forms',
    }
    return render(request, 'forms/form_list.html', context)


def form_detail(request, slug):
    """Display and handle form submission"""
    form_obj = get_object_or_404(Form, slug=slug, is_active=True)
    
    if request.method == 'POST':
        DynamicForm = create_dynamic_form(form_obj)
        form = DynamicForm(request.POST)
        
        if form.is_valid():
            # Create submission
            submission = FormSubmission.objects.create(
                form=form_obj,
                user_ip=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Store form data
            fields_dict = {field.label: field for field in form_obj.fields.all()}
            
            for field_label, value in form.cleaned_data.items():
                field = fields_dict.get(field_label)
                FormSubmissionData.objects.create(
                    submission=submission,
                    field=field,
                    field_label=field_label,
                    value=str(value)
                )
            
            # Send email notification if configured
            if form_obj.email_notification:
                send_form_submission_email(form_obj, submission)
            
            messages.success(request, f'Form "{form_obj.title}" submitted successfully!')
            return redirect('forms:success', submission_id=submission.id)
    else:
        DynamicForm = create_dynamic_form(form_obj)
        form = DynamicForm()
    
    context = {
        'form': form,
        'form_obj': form_obj,
        'page_title': form_obj.title,
    }
    return render(request, 'forms/form_detail.html', context)


def form_success(request, submission_id):
    """Success page after form submission"""
    submission = get_object_or_404(FormSubmission, id=submission_id)
    
    context = {
        'submission': submission,
        'form': submission.form,
        'page_title': 'Form Submitted',
    }
    return render(request, 'forms/form_success.html', context)


def send_form_submission_email(form_obj, submission):
    """Send email notification for form submission"""
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    
    try:
        subject = f'New Form Submission: {form_obj.title}'
        
        # Build email content
        email_content = f"Form: {form_obj.title}\n\n"
        email_content += "Submitted Data:\n"
        email_content += "-" * 50 + "\n\n"
        
        for data in submission.data.all():
            email_content += f"{data.field_label}: {data.value}\n"
        
        email_content += f"\n\nSubmitted at: {submission.submitted_at}\n"
        email_content += f"IP Address: {submission.user_ip}\n"
        
        send_mail(
            subject,
            email_content,
            'noreply@kyagreen.com',
            [form_obj.email_notification],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Error sending form submission email: {e}")
