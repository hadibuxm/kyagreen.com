import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiyagreen.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from products.models import Category, Product

# Create test data
cat1 = Category.objects.create(name="Debug Cat 1", slug="debug-cat-1", is_active=True)
prod1 = Product.objects.create(
    name="Debug Prod 1",
    slug="debug-prod-1",
    sku="debug-sku-1",
    category=cat1,
    description="test",
    main_image="test.jpg",
    is_active=True
)

cat2 = Category.objects.create(name="Debug Cat 2", slug="debug-cat-2", is_active=True)
prod2 = Product.objects.create(
    name="Debug Prod 2",
    slug="debug-prod-2",
    sku="debug-sku-2",
    category=cat2,
    description="test",
    main_image="test.jpg",
    is_active=True
)

# Test filtering
client = Client()

print("\n=== Testing Product Filtering ===\n")

print("1. All Products (no filter):")
response = client.get(reverse('products:list'))
print(f"   Status code: {response.status_code}")
if response.status_code == 200:
    count = response.context['products'].count()
    print(f"   Products shown: {count}")
    for p in response.context['products']:
        print(f"   - {p.name} (Category: {p.category.name})")
else:
    print(f"   Error: {response.content}")

print(f"\n2. Filter by '{cat1.name}':")
response = client.get(reverse('products:category', args=[cat1.slug]))
print(f"   Status code: {response.status_code}")
if response.status_code == 200:
    count = response.context['products'].count()
    selected = response.context['selected_category']
    print(f"   Selected category: {selected.name if selected else 'None'}")
    print(f"   Products shown: {count}")
    for p in response.context['products']:
        print(f"   - {p.name} (Category: {p.category.name})")

print(f"\n3. Filter by '{cat2.name}':")
response = client.get(reverse('products:category', args=[cat2.slug]))
print(f"   Status code: {response.status_code}")
if response.status_code == 200:
    count = response.context['products'].count()
    selected = response.context['selected_category']
    print(f"   Selected category: {selected.name if selected else 'None'}")
    print(f"   Products shown: {count}")
    for p in response.context['products']:
        print(f"   - {p.name} (Category: {p.category.name})")

# Cleanup
cat1.delete()
cat2.delete()
print("\n✓ Test completed and cleaned up")
