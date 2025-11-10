from django.shortcuts import render, redirect
from django.contrib import messages
from .models import HomePage, InformationPage, ContactInfo
from products.models import Product
from services.models import Service


def home(request):
    """Homepage view with featured products and services"""
    homepage = HomePage.load()
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    services = Service.objects.filter(is_active=True)[:3]

    context = {
        'homepage': homepage,
        'featured_products': featured_products,
        'services': services,
    }
    return render(request, 'core/home.html', context)


def information(request):
    """Information/About Us page"""
    info_page = InformationPage.load()

    context = {
        'info_page': info_page,
    }
    return render(request, 'core/information.html', context)


def contact(request):
    """Contact page"""
    contact_info = ContactInfo.load()

    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Here you would typically send an email or save to database
        # For now, just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')

    context = {
        'contact_info': contact_info,
    }
    return render(request, 'core/contact.html', context)
