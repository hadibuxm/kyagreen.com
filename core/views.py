from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import HomePage, InformationPage, ContactInfo
from products.models import Product, Category
from services.models import Service


def home(request):
    """Homepage view with featured products, categories, and trending products"""
    homepage = HomePage.load()
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    services = Service.objects.filter(is_active=True)[:3]
    
    # Get major categories (parent categories only)
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by('order')[:8]
    
    # Get trending products - products with most RFQ requests
    trending_products = Product.objects.filter(is_active=True).annotate(
        rfq_count=Count('rfq_requests')
    ).order_by('-rfq_count')[:6]

    context = {
        'homepage': homepage,
        'featured_products': featured_products,
        'services': services,
        'categories': categories,
        'trending_products': trending_products,
    }
    return render(request, 'core/home.html', context)


def search(request):
    """Global search for products and services"""
    query = request.GET.get('q', '').strip()
    products = []
    services = []
    
    if query:
        # Search products
        products = Product.objects.filter(
            is_active=True
        ).filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query)
        ).distinct()[:12]
        
        # Search services
        services = Service.objects.filter(
            is_active=True
        ).filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        ).distinct()[:12]
    
    context = {
        'query': query,
        'products': products,
        'services': services,
        'total_results': len(products) + len(services),
    }
    return render(request, 'core/search_results.html', context)


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
