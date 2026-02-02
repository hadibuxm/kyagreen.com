from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category
import logging

logger = logging.getLogger(__name__)


def product_list(request, slug=None):
    """Product listing with category filtering"""
    print(f"\n{'='*60}")
    print(f"📝 PRODUCT LIST VIEW CALLED")
    print(f"{'='*60}")
    print(f"📌 Received slug parameter: {slug}")
    print(f"📌 Request path: {request.path}")
    print(f"📌 Request GET params: {request.GET}")
    
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent=None)
    selected_category = None

    print(f"✅ Total active products: {products.count()}")
    print(f"✅ Total parent categories: {categories.count()}")

    # Filter by category if slug is provided
    if slug:
        print(f"\n🔍 FILTERING BY CATEGORY: {slug}")
        selected_category = get_object_or_404(Category, slug=slug, is_active=True)
        print(f"   ✅ Found category: {selected_category.name} (ID: {selected_category.id})")
        
        # Get products from selected category only
        products = products.filter(category=selected_category)
        print(f"   ✅ Products after filter: {products.count()}")
        for p in products:
            print(f"      - {p.name}")
    else:
        print(f"\n⚪ NO CATEGORY FILTER - showing all products")

    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        print(f"\n🔎 SEARCH QUERY: '{search_query}'")
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
        print(f"   ✅ Products after search: {products.count()}")

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    }
    
    print(f"\n📤 RENDERING TEMPLATE WITH:")
    print(f"   - Total products: {context['products'].count()}")
    print(f"   - Selected category: {context['selected_category'].name if context['selected_category'] else 'None'}")
    print(f"   - Search query: '{search_query}'")
    print(f"{'='*60}\n")
    
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
