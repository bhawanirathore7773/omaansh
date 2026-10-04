"""
SEO Template Tags for HOOVALE
Generates Schema.org JSON-LD markup for rich snippets in Google.

Usage in templates:
    {% load seo_tags %}
    {% local_business_schema %}
    {% organization_schema %}
    {% product_schema product %}
    {% breadcrumb_schema items %}
    {% faq_schema faqs %}
    {% review_schema testimonials %}
"""
import json
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.urls import reverse
from products.models import SiteSettings

register = template.Library()


# ============================================================
# HELPER: Render JSON-LD
# ============================================================
def render_jsonld(data):
    """Convert dict to <script type='application/ld+json'>"""
    return mark_safe(
        f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'
    )


# ============================================================
# 1. LOCAL BUSINESS SCHEMA (most important for local SEO)
# ============================================================
@register.simple_tag
def local_business_schema():
    """
    Outputs LocalBusiness schema. Critical for ranking in Jaipur.
    Use on every page (or at least homepage + contact).
    """
    s = SiteSettings.load()
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": "https://hoovale.com/#business",
        "name": s.business_name,
        "image": "https://hoovale.com/static/images/favicon/android-chrome-512x512.png",
        "description": s.default_meta_description,
        "url": "https://hoovale.com",
        "telephone": s.primary_phone,
        "email": s.email,
        "priceRange": "₹₹",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": s.street_address,
            "addressLocality": s.locality,
            "addressRegion": s.region,
            "postalCode": s.postal_code,
            "addressCountry": s.country,
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": s.latitude,
            "longitude": s.longitude,
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
                "opens": "09:00",
                "closes": "19:00"
            }
        ],
        "sameAs": [u for u in [s.facebook_url, s.instagram_url, s.youtube_url, s.linkedin_url] if u],
    }
    return render_jsonld(data)


# ============================================================
# 2. ORGANIZATION SCHEMA (brand entity)
# ============================================================
@register.simple_tag
def organization_schema():
    """Identifies HOOVALE as an organization in Google Knowledge Graph."""
    s = SiteSettings.load()
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": "https://hoovale.com/#organization",
        "name": s.business_name,
        "alternateName": "HOOVALE",
        "url": "https://hoovale.com/",
        "logo": {
            "@type": "ImageObject",
            "url": "https://hoovale.com/static/images/hoovale-mark.svg",
            "width": 600,
            "height": 200
        },
        "foundingDate": str(s.establishment_year),
        "description": s.default_meta_description,
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": s.primary_phone,
            "contactType": "Sales",
            "areaServed": "IN",
            "availableLanguage": ["English", "Hindi"]
        },
        "sameAs": [u for u in [s.facebook_url, s.instagram_url, s.youtube_url, s.linkedin_url] if u],
    }
    return render_jsonld(data)


# ============================================================
# 3. PRODUCT SCHEMA (rich snippets with price + rating)
# ============================================================
@register.simple_tag
def product_schema(product, request=None):
    """
    Outputs Product schema. Gives rich snippet with price, availability, rating.
    Usage: {% product_schema product %}
    """
    base_url = "https://hoovale.com"
    image_url = base_url + product.image.url if product.image else f"{base_url}/static/images/placeholder.jpg"

    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "image": image_url,
        "description": strip_tags(product.description)[:500],
        "sku": product.sku or f"HV-{product.id}",
        "brand": {
            "@type": "Brand",
            "name": product.brand or "HOOVALE"
        },
        "category": product.category.name if product.category else "Wall Clocks",
    }

    if product.price:
        data["offers"] = {
            "@type": "Offer",
            "url": base_url + product.get_absolute_url(),
            "priceCurrency": "INR",
            "price": str(product.price),
            "availability": f"https://schema.org/{product.availability}",
            "seller": {
                "@type": "Organization",
                "name": "HOOVALE"
            }
        }

    return render_jsonld(data)


# ============================================================
# 4. BREADCRUMB SCHEMA (improves CTR in search results)
# ============================================================
@register.simple_tag
def breadcrumb_schema(items):
    """
    Outputs BreadcrumbList schema.
    items = [('Name', 'url'), ('Name2', 'url2'), ...]
    """
    base_url = "https://hoovale.com"
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": base_url + url if url and not url.startswith('http') else url
            }
            for i, (name, url) in enumerate(items)
        ]
    }
    return render_jsonld(data)


# ============================================================
# 5. FAQ SCHEMA (powerful for rich snippets!)
# ============================================================
@register.simple_tag
def faq_schema(faqs):
    """
    Outputs FAQPage schema. Often shown as expandable Q&A in Google.
    Usage: {% faq_schema faqs %}
    """
    if not faqs:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq.question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": strip_tags(faq.answer)
                }
            }
            for faq in faqs
        ]
    }
    return render_jsonld(data)


# ============================================================
# 6. REVIEW / AGGREGATE RATING SCHEMA
# ============================================================
@register.simple_tag
def aggregate_rating_schema(testimonials):
    """
    Computes average rating from testimonials and outputs schema.
    Shows ★ rating in Google search results.
    """
    if not testimonials:
        return ""

    ratings = [t.rating for t in testimonials if t.rating]
    if not ratings:
        return ""

    avg = round(sum(ratings) / len(ratings), 1)
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "HOOVALE Wall Clocks",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(avg),
            "reviewCount": str(len(ratings)),
            "bestRating": "5",
            "worstRating": "1"
        }
    }
    return render_jsonld(data)


# ============================================================
# 7. WEBSITE SCHEMA
# ============================================================
@register.simple_tag
def website_schema():
    """Outputs WebSite entity markup for site identity."""
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": "https://hoovale.com/#website",
        "url": "https://hoovale.com/",
        "name": "HOOVALE",
        "alternateName": "HOOVALE Wall Clocks",
        "publisher": {"@id": "https://hoovale.com/#organization"}
    }
    return render_jsonld(data)


# ============================================================
# 8. SITE NAVIGATION SCHEMA
# ============================================================
@register.simple_tag
def site_navigation_schema():
    """Outputs navigation links so crawlers can understand site hierarchy."""
    links = [
        ("Home", "/"),
        ("Wall Clocks", "/products/"),
        ("Categories", "/categories/"),
        ("Services", "/services/"),
        ("About HOOVALE", "/about/"),
        ("Wall Clock Guides", "/blog/"),
        ("Contact", "/contact/"),
    ]
    base_url = "https://hoovale.com"
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "HOOVALE site navigation",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "url": base_url + url
            }
            for i, (name, url) in enumerate(links)
        ]
    }
    return render_jsonld(data)


# ============================================================
# 8. SITE SETTINGS ACCESS
# ============================================================
@register.simple_tag
def get_site_settings():
    """Get site settings object in any template."""
    return SiteSettings.load()


# ============================================================
# 9. HELPER: Render breadcrumbs HTML
# ============================================================
@register.inclusion_tag('components/breadcrumbs.html')
def render_breadcrumbs(items):
    """
    Render visual breadcrumbs.
    items = [('Home', '/'), ('Products', '/products/'), ('Current', None)]
    """
    return {'items': items}


# ============================================================
# 10. CANONICAL URL
# ============================================================
@register.simple_tag(takes_context=True)
def canonical_url(context):
    """Generates canonical URL for current page."""
    request = context.get('request')
    if not request:
        return ''
    return request.build_absolute_uri(request.path)


# ============================================================
# 11. WHATSAPP LINK GENERATOR
# ============================================================
@register.simple_tag
def whatsapp_link(message=''):
    """Generates pre-filled WhatsApp link."""
    s = SiteSettings.load()
    from urllib.parse import quote
    return f"https://wa.me/{s.whatsapp_number}?text={quote(message)}"


# ============================================================
# 12. CALL LINK GENERATOR
# ============================================================
@register.simple_tag
def call_link():
    """Generates tel: link from site settings."""
    s = SiteSettings.load()
    return f"tel:{s.primary_phone}"


# ============================================================
# 13. META TAG GENERATOR (consolidates all meta tags)
# ============================================================
@register.inclusion_tag('components/meta_tags.html', takes_context=True)
def seo_meta(context, title=None, description=None, keywords=None, image=None, url=None):
    """
    One tag to render all meta tags.
    Usage: {% seo_meta title=product.meta_title description=product.meta_description %}
    """
    request = context.get('request')
    s = SiteSettings.load()

    return {
        'title': title or s.default_meta_title,
        'description': (description or s.default_meta_description)[:160],
        'keywords': keywords or 'wall clock manufacturer jaipur, bulk wall clocks, wholesale clocks',
        'image': image or 'https://hoovale.com/static/images/og-default.jpg',
        'url': url or (request.build_absolute_uri() if request else 'https://hoovale.com'),
        'business_name': s.business_name,
    }
