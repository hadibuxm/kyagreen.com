#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kiyagreen.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()

print('Test 1: All products')
response = client.get(reverse('products:list'))
print(f'  Products count: {response.context["products"].count()}')
print(f'  Selected category: {response.context["selected_category"]}')

print('\nTest 2: Filter by C1')
response = client.get(reverse('products:category', args=['c1']))
print(f'  Products count: {response.context["products"].count()}')
print(f'  Selected category: {response.context["selected_category"]}')
for p in response.context['products']:
    print(f'    - {p.name}')

print('\nTest 3: Filter by C11')
response = client.get(reverse('products:category', args=['c11']))
print(f'  Products count: {response.context["products"].count()}')
print(f'  Selected category: {response.context["selected_category"]}')
for p in response.context['products']:
    print(f'    - {p.name}')
