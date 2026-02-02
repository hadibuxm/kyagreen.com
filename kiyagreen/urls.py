"""
URL configuration for kiyagreen project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.home, name="home"),
    path("search/", core_views.search, name="search"),
    path("information/", core_views.information, name="information"),
    path("contact/", core_views.contact, name="contact"),
    path("products/", include("products.urls")),
    path("services/", include("services.urls")),
    path("rfq/", include("rfq.urls")),
    path("forms/", include("forms.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "KiyaGreen Administration"
admin.site.site_title = "KiyaGreen Admin"
admin.site.index_title = "Welcome to KiyaGreen Administration"
