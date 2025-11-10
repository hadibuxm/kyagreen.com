from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category


def product_list(request, slug=None):
    """Product listing with category filtering"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent=None)
    selected_category = None

    # Filter by category if slug is provided
    if slug:
        selected_category = get_object_or_404(Category, slug=slug, is_active=True)
        # Get products from selected category and its children
        category_ids = [selected_category.id]
        category_ids.extend(selected_category.children.values_list('id', flat=True))
        products = products.filter(category__id__in=category_ids)

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Increment view count
    product.views += 1
    product.save(update_fields=['views'])

    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def product_search(request):
    """AJAX product search for autocomplete"""
    query = request.GET.get('q', '')
    products = []

    if query and len(query) >= 2:
        products_qs = Product.objects.filter(
            Q(name__icontains=query) | Q(sku__icontains=query),
            is_active=True
        )[:10]

        products = [{'id': p.id, 'name': p.name, 'sku': p.sku} for p in products_qs]

    return JsonResponse(products, safe=False)
