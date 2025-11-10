from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .forms import RFQRequestForm


def rfq_create(request):
    """General RFQ form"""
    if request.method == 'POST':
        form = RFQRequestForm(request.POST, request.FILES)
        if form.is_valid():
            rfq = form.save()
            messages.success(request, 'Your request for quotation has been submitted successfully! We will contact you soon.')
            return redirect('rfq:success')
    else:
        form = RFQRequestForm()

    context = {
        'form': form,
        'page_title': 'Request for Quotation',
    }
    return render(request, 'rfq/rfq_form.html', context)


def rfq_create_for_product(request, product_id):
    """RFQ form pre-filled with a specific product"""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        form = RFQRequestForm(request.POST, request.FILES, product_id=product_id)
        if form.is_valid():
            rfq = form.save()
            messages.success(request, f'Your request for quotation for "{product.name}" has been submitted successfully!')
            return redirect('rfq:success')
    else:
        form = RFQRequestForm(product_id=product_id)

    context = {
        'form': form,
        'product': product,
        'page_title': f'Request Quote for {product.name}',
    }
    return render(request, 'rfq/rfq_form.html', context)


def rfq_success(request):
    """Success page after RFQ submission"""
    return render(request, 'rfq/rfq_success.html')
