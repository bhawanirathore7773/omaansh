"""
Dynamic XML Sitemaps for HOOVALE
All URL types auto-included → submit to Google Search Console
URL: /sitemap.xml
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product, Category, CityPage, IndustryPage, ServicePage, Blog, Banner


class StaticViewSitemap(Sitemap):
    """Static pages: home, about, contact, etc."""
    priority = 1.0
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'home',
            'about',
            'contact',
            'products_list',
            'categories_index',
            'services_index',
            'cities_index',
            'industries_index',
            'blog_list',
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    """All active products"""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    """All product categories"""
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CityPageSitemap(Sitemap):
    """City landing pages — HIGH PRIORITY for local SEO"""
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return CityPage.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class IndustryPageSitemap(Sitemap):
    """Industry-specific landing pages"""
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return IndustryPage.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class ServicePageSitemap(Sitemap):
    """Service pages: OEM, Bulk, Customization"""
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ServicePage.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    """Blog posts"""
    changefreq = 'monthly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at



class BannerSitemap(Sitemap):
    """Published collection landing pages linked from homepage campaigns."""
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Banner.objects.filter(is_active=True, is_page_published=True)

    def lastmod(self, obj):
        # Banner has created_at only; use it for sitemap lastmod.
        return getattr(obj, 'updated_at', None) or getattr(obj, 'created_at', None)

# Combined dict — register in main urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'cities': CityPageSitemap,
    'industries': IndustryPageSitemap,
    'services': ServicePageSitemap,
    'banners': BannerSitemap,
    'blog': BlogSitemap,
}
