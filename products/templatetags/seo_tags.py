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
@register.simple_tag(takes_context=True)
def local_business_schema(context):
    """
    Outputs LocalBusiness schema. Critical for ranking in Jaipur.
    Use on every page (or at least homepage + contact).
    """
    s = SiteSettings.load()
    request = context.get("request")
    origin = request.build_absolute_uri("/").rstrip("/") if request else ""
    logo_url = request.build_absolute_uri("/static/images/favicon/android-chrome-512x512.png") if request else "/static/images/favicon/android-chrome-512x512.png"
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{origin}/#business" if origin else "#business",
        "name": s.business_name,
        "image": logo_url,
        "description": s.default_meta_description,
        "url": origin or "/",
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
@register.simple_tag(takes_context=True)
def organization_schema(context):
    """Identifies HOOVALE as an organization in Google Knowledge Graph."""
    s = SiteSettings.load()
    request = context.get("request")
    origin = request.build_absolute_uri("/").rstrip("/") if request else ""
    logo_url = request.build_absolute_uri("/static/images/favicon/android-chrome-512x512.png") if request else "/static/images/favicon/android-chrome-512x512.png"
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{origin}/#organization" if origin else "#organization",
        "name": s.business_name,
        "url": origin or "/",
        "logo": {
            "@type": "ImageObject",
            "url": logo_url,
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
    request = context.get("request")
    base_url = request.build_absolute_uri("/").rstrip("/") if request else ""
    image_url = (base_url + product.image.url) if product.image else f"{base_url}/static/images/product-placeholder.svg"

    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product.name,
        "image": image_url,
        "description": strip_tags(product.description)[:500],
        "sku": product.sku or f"HV-{product.id}",
        "brand": {
            "@type": "Brand",
            "name": product.brand or SiteSettings.load().business_name
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
                "name": SiteSettings.load().business_name
            }
        }

    return render_jsonld(data)


# ============================================================
# 4. BREADCRUMB SCHEMA (improves CTR in search results)
# ============================================================
@register.simple_tag(takes_context=True)
def breadcrumb_schema(context, items):
    """
    Outputs BreadcrumbList schema.
    items = [('Name', 'url'), ('Name2', 'url2'), ...]
    """
    base_url = request.build_absolute_uri("/").rstrip("/") if request else ""
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
@register.simple_tag(takes_context=True)
def website_schema(context):
    """Outputs a dynamic WebSite entity using the current request origin."""
    s = SiteSettings.load()
    request = context.get("request")
    origin = request.build_absolute_uri("/").rstrip("/") if request else ""
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{origin}/#website" if origin else "#website",
        "url": origin or "/",
        "name": s.business_name,
        "publisher": {"@id": f"{origin}/#organization" if origin else "#organization"}
    }
    return render_jsonld(data)


# ============================================================
# 8. SITE NAVIGATION SCHEMA
# ============================================================
@register.simple_tag(takes_context=True)
def site_navigation_schema(context):
    """Outputs navigation markup using the site's real origin."""
    s = SiteSettings.load()
    request = context.get("request")
    origin = request.build_absolute_uri("/").rstrip("/") if request else ""
    links = [
        ("Home", "/"),
        ("Wall Clocks", "/products/"),
        ("Collections", "/categories/"),
        ("Services", "/services/"),
        ("About", "/about/"),
        ("Guides", "/blog/"),
        ("Contact", "/contact/"),
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{s.business_name} site navigation",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "url": f"{origin}{url}"}
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
        'image': image or (request.build_absolute_uri('/static/images/og-default.jpg') if request else '/static/images/og-default.jpg'),
        'url': url or (request.build_absolute_uri() if request else ''),
        'business_name': s.business_name,
    }
