from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    path('', views.form_list, name='list'),
    path('<slug:slug>/', views.form_detail, name='detail'),
    path('success/<int:submission_id>/', views.form_success, name='success'),
]
