from django.urls import path
from . import views

app_name = 'rfq'

urlpatterns = [
    path('', views.rfq_create, name='create'),
    path('product/<int:product_id>/', views.rfq_create_for_product, name='create_for_product'),
    path('success/', views.rfq_success, name='success'),
]
