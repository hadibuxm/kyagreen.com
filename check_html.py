import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiyagreen.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()
response = client.get(reverse('products:list'))

if response.status_code == 200:
    html = response.content.decode()
    
    # Check if category links are in the HTML
    if '<a href="/products/category/' in html:
        print("✅ Category links ARE being rendered in HTML")
        # Count them
        count = html.count('<a href="/products/category/')
        print(f"   Found {count} category links")
    else:
        print("❌ Category links are NOT being rendered")
    
    # Check if render_category_tree is being called
    if '{% render_category_tree' in html:
        print("❌ Template tag NOT compiled (still showing template code)")
    else:
        print("✅ Template tag IS compiled")
        
    print("\nCategory section of HTML:")
    start = html.find('<h6>Categories</h6>')
    if start > 0:
        end = start + 2000
        section = html[start:end]
        print(section)
    else:
        print("Could not find Categories section")
else:
    print(f"Error: Status code {response.status_code}")
