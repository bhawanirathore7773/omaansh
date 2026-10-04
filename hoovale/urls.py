"""
HOOVALE Project URLs (hoovale/urls.py)
Phase 1: Adds sitemap framework
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from accounts import views as accounts_views
from products.sitemaps import sitemaps

urlpatterns = [
    path('admin/login/', accounts_views.admin_login, name='admin_login'),
    path('admin/forgot-password/', accounts_views.admin_forgot_password, name='admin_forgot_password'),
    path('admin/', admin.site.urls),

    # Sitemap framework — Google Search Console will crawl this
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    # App URLs
    path('', include('products.urls')),
    path('', include('enquiries.urls')),
]

# Media files in development
# Serve uploaded media files on the Render web service as well.
# Render Free is fine for testing; for production, move media to object storage.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'products.views.page_not_found'
handler500 = 'products.views.server_error'
