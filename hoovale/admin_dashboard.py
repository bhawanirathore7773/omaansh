from django.contrib.auth import get_user_model
from django.utils import timezone

from products.models import (
    Product, Category, Blog, CityPage, IndustryPage,
    ServicePage, FAQ, Testimonial, Banner, SiteSettings,
    PricingTierTemplate,
)
from enquiries.models import Enquiry


def _count(queryset):
    """Return a dashboard count without allowing one optional metric to break /admin/."""
    try:
        return queryset.count()
    except Exception:
        return 0


def _exists(queryset):
    """Return a dashboard existence flag without breaking the admin dashboard."""
    try:
        return queryset.exists()
    except Exception:
        return False


def _slice(queryset, limit=8):
    """Return a safe queryset/list for dashboard widgets."""
    try:
        return list(queryset[:limit])
    except Exception:
        return []


def dashboard_callback(request, context):
    """
    Prepare lightweight admin dashboard metrics.

    The dashboard must never return HTTP 500 just because an optional
    content table/query is unavailable during a deployment or migration.
    """
    now = timezone.now()
    month_start = now.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    User = get_user_model()

    context.update(
        {
            "dashboard": {
                "products": _count(Product.objects.all()),
                "active_products": _count(
                    Product.objects.filter(is_active=True)
                ),
                "categories": _count(Category.objects.all()),
                "enquiries": _count(Enquiry.objects.all()),
                "new_enquiries": _count(
                    Enquiry.objects.filter(status="new")
                ),
                "published_blogs": _count(
                    Blog.objects.filter(is_published=True)
                ),
                "city_pages": _count(
                    CityPage.objects.filter(is_published=True)
                ),
                "industry_pages": _count(
                    IndustryPage.objects.filter(is_published=True)
                ),
                "services": _count(
                    ServicePage.objects.filter(is_published=True)
                ),
                "faqs": _count(
                    FAQ.objects.filter(is_active=True)
                ),
                "testimonials": _count(
                    Testimonial.objects.filter(is_active=True)
                ),
                "banners": _count(
                    Banner.objects.filter(is_active=True)
                ),
                "users": _count(User.objects.all()),
                "site_settings": _exists(SiteSettings.objects.all()),
                "pricing_templates": _count(
                    PricingTierTemplate.objects.filter(is_active=True)
                ),
                "monthly_enquiries": _count(
                    Enquiry.objects.filter(created_at__gte=month_start)
                ),
            },
            "recent_enquiries": _slice(
                Enquiry.objects.select_related("product").order_by(
                    "-created_at"
                ),
                8,
            ),
            "recent_products": _slice(
                Product.objects.select_related("category").order_by(
                    "-created_at"
                ),
                6,
            ),
            "recent_blogs": _slice(
                Blog.objects.order_by("-created_at"),
                5,
            ),
            "new_enquiries": _slice(
                Enquiry.objects.filter(status="new").order_by(
                    "-created_at"
                ),
                5,
            ),
        }
    )

    return context
