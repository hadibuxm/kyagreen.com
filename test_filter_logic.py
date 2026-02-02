import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiyagreen.settings')
django.setup()

from products.models import Product, Category
from django.test import Client
from django.urls import reverse

client = Client()

print("\n=== TESTING FILTERING LOGIC ===\n")

# Test 1: All products
response = client.get(reverse('products:list'))
if response.context:
    products = response.context['products']
    print(f"1. ALL PRODUCTS (/products/):")
    print(f"   Count: {products.count()}")
    for p in products:
        print(f"   - {p.name} (category: {p.category.name})")
else:
    print("ERROR: Response context is None")

# Test 2: C1 category
response = client.get(reverse('products:category', args=['c1']))
if response.context:
    products = response.context['products']
    selected = response.context['selected_category']
    print(f"\n2. FILTER BY '{selected.name}' (/products/category/c1/):")
    print(f"   Count: {products.count()}")
    for p in products:
        print(f"   - {p.name} (category: {p.category.name})")
else:
    print("ERROR: Response context is None")

# Test 3: C11 category
response = client.get(reverse('products:category', args=['c11']))
if response.context:
    products = response.context['products']
    selected = response.context['selected_category']
    print(f"\n3. FILTER BY '{selected.name}' (/products/category/c11/):")
    print(f"   Count: {products.count()}")
    for p in products:
        print(f"   - {p.name} (category: {p.category.name})")
else:
    print("ERROR: Response context is None")

print("\n=== ANALYSIS ===")
print("If filtering is NOT working correctly:")
print("  - All 6 products appear in every filter")
print("  - The view logic may have been accidentally reverted")
print("\nIf filtering IS working correctly:")
print("  - C1 filter shows 1 product (P1)")
print("  - C11 filter shows 1 product (P2)")
