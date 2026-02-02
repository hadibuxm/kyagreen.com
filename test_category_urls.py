import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiyagreen.settings')
django.setup()

from products.models import Product, Category
from django.urls import reverse

print("\n=== URL GENERATION TEST ===\n")

# Get categories
for cat in Category.objects.filter(is_active=True, parent__isnull=True):
    url = reverse('products:category', args=[cat.slug])
    products_count = Product.objects.filter(category=cat, is_active=True).count()
    print(f"Category: {cat.name}")
    print(f"  Slug: {cat.slug}")
    print(f"  URL: {url}")
    print(f"  Products: {products_count}")
    print()

# Simulate what happens when clicking on a category
print("\n=== SIMULATING VIEW BEHAVIOR ===\n")
from django.test import RequestFactory
from products.views import product_list

factory = RequestFactory()

# Get first category
first_cat = Category.objects.filter(is_active=True, parent__isnull=True).first()
if first_cat:
    print(f"Testing with category: {first_cat.name} (slug: {first_cat.slug})\n")
    
    # Create a GET request to the category URL
    url = reverse('products:category', args=[first_cat.slug])
    request = factory.get(url)
    
    # Call the view
    response = product_list(request, slug=first_cat.slug)
    
    print(f"Response status: {response.status_code}")
    # Can't access context directly from response object in this way
    # Let's use Django test client instead
    
from django.test import Client

client = Client()
response = client.get(url)

if response.context:
    print(f"\nTest Result:")
    print(f"  URL accessed: {url}")
    print(f"  Selected category: {response.context['selected_category']}")
    print(f"  Products count: {response.context['products'].count()}")
    print(f"  Products:")
    for p in response.context['products']:
        print(f"    - {p.name} (category: {p.category.name})")
else:
    print("ERROR: Response context is None")
