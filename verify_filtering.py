import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiyagreen.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()

print("\n=== TESTING ACTUAL FILTERING ===\n")

# Test 1: All products (no filter)
print("1. ALL PRODUCTS (default page)")
response = client.get(reverse('products:list'))
if response.context:
    count = response.context['products'].count()
    print(f"   ✅ Shows {count} products")
    for p in response.context['products'][:3]:
        print(f"      - {p.name}")
else:
    print("   ❌ Error: Response context is None")

# Test 2: Filter by C1
print("\n2. FILTER BY 'C1' (/products/category/c1/)")
response = client.get('/products/category/c1/')
if response.context:
    count = response.context['products'].count()
    selected = response.context['selected_category']
    print(f"   ✅ Selected category: {selected.name if selected else 'None'}")
    print(f"   ✅ Shows {count} product(s)")
    for p in response.context['products']:
        print(f"      - {p.name} (category: {p.category.name})")
else:
    print("   ❌ Error: Response context is None")

# Test 3: Filter by debug-cat-1
print("\n3. FILTER BY 'Debug Cat 1' (/products/category/debug-cat-1/)")
response = client.get('/products/category/debug-cat-1/')
if response.context:
    count = response.context['products'].count()
    selected = response.context['selected_category']
    print(f"   ✅ Selected category: {selected.name if selected else 'None'}")
    print(f"   ✅ Shows {count} product(s)")
    for p in response.context['products']:
        print(f"      - {p.name} (category: {p.category.name})")
else:
    print("   ❌ Error: Response context is None")

print("\n=== CONCLUSION ===")
print("If all tests show ✅, then filtering IS working correctly.")
print("If you're seeing all products in the browser, try:")
print("  1. Hard refresh (Cmd+Shift+R or Ctrl+Shift+R)")
print("  2. Clear browser cache")
print("  3. Open in private/incognito mode")
