"""
HOOVALE Views - Phase 1 SEO Foundation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from .models import (
    Product, Category, Blog, CityPage, IndustryPage,
    ServicePage, FAQ, Testimonial, Banner, SiteSettings
)


# ============================================================
# HOMEPAGE
# ============================================================
def home(request):
    site = SiteSettings.load()
    all_banners = Banner.objects.filter(is_active=True).order_by('order', 'created_at')
    website_banners = all_banners.filter(banner_type='website')
    mobile_banners = all_banners.filter(banner_type='mobile')
    # New campaign records carry both desktop and mobile images. Keep the
    # legacy banner_type split compatible, but never render an empty carousel.
    if not website_banners.exists():
        website_banners = all_banners
    if not mobile_banners.exists():
        mobile_banners = website_banners

    # Always keep the homepage campaign carousel populated with four
    # production-safe banners. Admin-managed banners are used first; if fewer
    # than four are configured, curated static campaign artwork fills the gaps.
    homepage_campaigns = []
    for banner in website_banners[:4]:
        homepage_campaigns.append({
            'url': banner.get_absolute_url(),
            'title': banner.title,
            'heading': banner.heading,
            'subheading': banner.subheading,
            'cta_text': banner.cta_text,
            'desktop_url': banner.homepage_desktop_url,
            'mobile_url': banner.homepage_mobile_url,
            'is_dynamic': True,
        })

    static_campaigns = [
        {
            'url': '/products/',
            'title': 'Wedding Gifts',
            'heading': 'Personalized Wall Clocks',
            'subheading': 'Customized clocks for weddings, gifting and special moments.',
            'cta_text': 'Explore Collection',
            'desktop_url': '/static/images/banners/wedding-desktop.svg',
            'mobile_url': '/static/images/banners/wedding-mobile.svg',
            'is_dynamic': False,
        },
        {
            'url': '/products/',
            'title': 'Corporate Clocks',
            'heading': 'Corporate & Branded Wall Clocks',
            'subheading': 'Professional clocks with your logo for offices, gifting and brand promotion.',
            'cta_text': 'Explore Corporate',
            'desktop_url': '/static/images/banners/corporate-desktop.svg',
            'mobile_url': '/static/images/banners/corporate-mobile.svg',
            'is_dynamic': False,
        },
        {
            'url': '/products/',
            'title': 'Custom Wall Clocks',
            'heading': 'Custom Wall Clocks for Your Brand',
            'subheading': 'Choose designs, branding and quantities for your business requirements.',
            'cta_text': 'Customize Now',
            'desktop_url': '/static/images/banners/custom-desktop.svg',
            'mobile_url': '/static/images/banners/custom-mobile.svg',
            'is_dynamic': False,
        },
        {
            'url': '/products/',
            'title': 'Promotional Clocks',
            'heading': 'Promotional Wall Clocks',
            'subheading': 'Logo-branded clocks for marketing campaigns, dealers and business promotion.',
            'cta_text': 'Get a Quote',
            'desktop_url': '/static/images/banners/promotion-desktop.svg',
            'mobile_url': '/static/images/banners/promotion-mobile.svg',
            'is_dynamic': False,
        },
    ]
    for campaign in static_campaigns:
        if len(homepage_campaigns) >= 4:
            break
        homepage_campaigns.append({**campaign, 'is_dynamic': False})

    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    new_arrivals = Product.objects.filter(is_active=True, is_new_arrival=True).order_by('-created_at')[:8]
    if not new_arrivals.exists():
        new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:8]

    bestseller_products = Product.objects.filter(
        is_active=True, is_bestseller=True
    ).order_by('-updated_at', '-created_at')[:8]

    custom_products = Product.objects.filter(
        is_active=True
    ).filter(
        Q(category__name__icontains='custom') |
        Q(category__name__icontains='promotional') |
        Q(category__name__icontains='corporate')
    ).order_by('-is_featured', '-created_at')[:8]

    categories = Category.objects.filter(is_featured=True).order_by('display_order', 'name')[:8]

    # Marketplace-style homepage product shelves: each featured category
    # gets its own small product rail so buyers can scan products quickly.
    category_product_sections = []
    for category in categories[:5]:
        section_products = Product.objects.filter(
            is_active=True, category=category
        ).order_by('-is_featured', '-is_bestseller', '-created_at')[:4]
        if section_products.exists():
            category_product_sections.append({
                'category': category,
                'products': section_products,
            })

    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:6]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'home'])[:8]
    industries = IndustryPage.objects.filter(is_published=True)[:6]
    cities = CityPage.objects.filter(is_published=True)[:8]
    latest_blogs = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]

    context = {
        'site': site,
        'website_banners': website_banners,
        'mobile_banners': mobile_banners,
        'homepage_campaigns': homepage_campaigns,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'bestseller_products': bestseller_products,
        'custom_products': custom_products,
        'categories': categories,
        'category_product_sections': category_product_sections,
        'testimonials': testimonials,
        'faqs': faqs,
        'industries': industries,
        'cities': cities,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'products/home.html', context)


# ============================================================
# CATEGORIES
# ============================================================
def categories_index(request):
    """Render the marketplace-style category catalogue."""
    categories = Category.objects.all().order_by('display_order', 'name')
    return render(request, 'products/categories_index.html', {'categories': categories})


# ============================================================
# PRODUCTS
# ============================================================
def products_list(request):
    """Marketplace-style product catalogue with search + practical filters."""
    from django.db.models import Min, Max

    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all().order_by('display_order', 'name')

    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )

    selected_category = request.GET.get('category', '').strip()
    if selected_category:
        products = products.filter(category__slug=selected_category)

    # Price range. Keep empty values valid so "Clear all" is always safe.
    price_bounds = products.aggregate(min_price=Min('price'), max_price=Max('price'))
    catalogue_min_price = int(price_bounds['min_price'] or 0)
    catalogue_max_price = int(price_bounds['max_price'] or 0)

    min_price_raw = request.GET.get('min_price', '').strip()
    max_price_raw = request.GET.get('max_price', '').strip()
    try:
        min_price = max(0, int(float(min_price_raw))) if min_price_raw else ''
    except (TypeError, ValueError):
        min_price = ''
    try:
        max_price = max(0, int(float(max_price_raw))) if max_price_raw else ''
    except (TypeError, ValueError):
        max_price = ''

    if min_price != '':
        products = products.filter(price__gte=min_price)
    if max_price != '':
        products = products.filter(price__lte=max_price)

    availability = request.GET.get('availability', '').strip()
    if availability in {'InStock', 'OutOfStock', 'PreOrder'}:
        products = products.filter(availability=availability)

    badge = request.GET.get('badge', '').strip()
    if badge == 'featured':
        products = products.filter(is_featured=True)
    elif badge == 'bestseller':
        products = products.filter(is_bestseller=True)
    elif badge == 'new':
        products = products.filter(is_new_arrival=True)

    sort = request.GET.get('sort', 'featured').strip()
    sort_map = {
        'featured': ['-is_featured', '-created_at'],
        'newest': ['-created_at'],
        'price_low': ['price', '-created_at'],
        'price_high': ['-price', '-created_at'],
        'name': ['name'],
    }
    if sort not in sort_map:
        sort = 'featured'
    products = products.order_by(*sort_map[sort])

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    products_page = paginator.get_page(page_number)

    context = {
        'products': products_page,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
        'catalogue_min_price': catalogue_min_price,
        'catalogue_max_price': catalogue_max_price,
        'availability': availability,
        'badge': badge,
        'sort': sort,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Wall Clocks', None),
        ],
        'current_page': int(page_number) if str(page_number).isdigit() else 1,
        'total_pages': paginator.num_pages,
    }
    return render(request, 'products/products_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'product'])[:6]

    # ── Specifications ────────────────────────────────────────
    specifications = []
    if product.specifications:
        for line in product.specifications.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                specifications.append({
                    "key": key.strip(),
                    "value": value.strip()
                })

    # ── Pricing Tiers ─────────────────────────────────────────
    # Resolves the 5-tier structure via: custom JSON > template > default template > fallback
    base_price = float(product.price) if product.price else 0

    # Call get_pricing_tiers() if the method exists on the model,
    # otherwise use the inline fallback below (safe before migration).
    if hasattr(product, 'get_pricing_tiers'):
        raw_tiers = product.get_pricing_tiers()
    else:
        # Inline fallback — remove once migration is applied
        raw_tiers = [
            {'tier': 1, 'min_qty': 1,   'max_qty': 49,    'label': 'Sample / Trial', 'discount_type': 'percent', 'discount_value': 0,  'badge': 'MRP'},
            {'tier': 2, 'min_qty': 50,  'max_qty': 99,    'label': 'Small Order',    'discount_type': 'percent', 'discount_value': 5,  'badge': '5% OFF'},
            {'tier': 3, 'min_qty': 100, 'max_qty': 249,   'label': 'Standard Bulk',  'discount_type': 'percent', 'discount_value': 10, 'badge': '10% OFF'},
            {'tier': 4, 'min_qty': 250, 'max_qty': 499,   'label': 'Large Order',    'discount_type': 'percent', 'discount_value': 15, 'badge': '15% OFF'},
            {'tier': 5, 'min_qty': 500, 'max_qty': 99999, 'label': 'Wholesale / OEM','discount_type': 'percent', 'discount_value': 22, 'badge': 'Best Price'},
        ]

    # Enrich each tier with computed prices for template rendering
    pricing_tiers = []
    for t in raw_tiers:
        dv = float(t.get('discount_value', 0))
        if t.get('discount_type') == 'percent':
            saving = base_price * dv / 100
        else:
            saving = dv
        unit_price = max(0, base_price - saving)
        max_qty = t.get('max_qty', 99999)
        pricing_tiers.append({
            **t,
            'unit_price':        round(unit_price, 2),
            'saving_per_piece':  round(saving, 2),
            'max_qty_display':   f"{t['min_qty']}+" if max_qty >= 99999 else f"{t['min_qty']}–{max_qty}",
        })

    context = {
        'product':           product,
        'related_products':  related_products,
        'specifications':    specifications,
        'faqs':              faqs,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Products', '/products/'),
            (product.category.name, product.category.get_absolute_url()),
            (product.name, None),
        ],
        # Pricing tier context — used by template + injected as JSON for JS
        'pricing_tiers':      pricing_tiers,
        'pricing_tiers_json': json.dumps(pricing_tiers),
        'base_price':         base_price,
        'base_price_json':    json.dumps(base_price),
    }
    return render(request, 'products/product_detail.html', context)


def banner_page(request, slug):
    """Render the dynamic page behind a homepage campaign banner."""
    banner = get_object_or_404(
        Banner,
        slug=slug,
        is_active=True,
        is_page_published=True,
    )
    products = banner.page_products.filter(is_active=True).order_by(
        '-is_featured', '-is_bestseller', '-created_at'
    )
    if not products.exists():
        # A banner without explicit selections still works; admin can later
        # curate the exact products for that campaign.
        products = Product.objects.filter(is_active=True).order_by(
            '-is_featured', '-is_bestseller', '-created_at'
        )[:8]

    context = {
        'banner': banner,
        'products': products[:12],
        'page_title': banner.seo_title or banner.page_heading or banner.title,
        'page_description': banner.seo_description,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Collections', '/#collections'),
            (banner.page_heading or banner.title, None),
        ],
    }
    return render(request, 'products/banner_page.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    products_page = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': products_page,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Products', '/products/'),
            (category.name, None),
        ],
    }
    return render(request, 'products/category_detail.html', context)


# ============================================================
# CITY LANDING PAGES (Programmatic SEO)
# ============================================================
def city_landing(request, slug):
    city = get_object_or_404(CityPage, slug=slug, is_published=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:6]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'city'])[:6]

    # Static benefits for the cards section
    benefits = [
        {'icon': 'fas fa-industry', 'title': 'Direct Factory', 'desc': 'No middlemen — best wholesale prices'},
        {'icon': 'fas fa-truck-fast', 'title': 'Fast Delivery', 'desc': f'{city.delivery_time} to {city.city_name}'},
        {'icon': 'fas fa-paint-brush', 'title': 'Custom Logo', 'desc': 'Branded clocks with your logo'},
        {'icon': 'fas fa-shield-alt', 'title': 'Quality Assured', 'desc': '1 year warranty on all products'},
    ]

    context = {
        'city': city,
        'featured_products': featured_products,
        'faqs': faqs,
        'benefits': benefits,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Locations', '/locations/'),
            (city.h1_heading, None),
        ],
    }
    return render(request, 'products/city_landing.html', context)


def cities_index(request):
    """Index page listing all city landing pages."""
    cities = CityPage.objects.filter(is_published=True).order_by('display_order', 'city_name')
    return render(request, 'products/cities_index.html', {'cities': cities})


# ============================================================
# INDUSTRY PAGES
# ============================================================
def industry_page(request, slug):
    industry = get_object_or_404(IndustryPage, slug=slug, is_published=True)
    products = industry.featured_products.filter(is_active=True)[:8]
    if not products.exists():
        products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'industry'])[:6]

    context = {
        'industry': industry,
        'products': products,
        'faqs': faqs,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Industries', '/industries/'),
            (industry.industry_name, None),
        ],
    }
    return render(request, 'products/industry_page.html', context)


def industries_index(request):
    industries = IndustryPage.objects.filter(is_published=True).order_by('display_order', 'industry_name')
    return render(request, 'products/industries_index.html', {'industries': industries})


# ============================================================
# SERVICE PAGES
# ============================================================
def service_page(request, slug):
    service = get_object_or_404(ServicePage, slug=slug, is_published=True)
    related_services = ServicePage.objects.filter(is_published=True).exclude(id=service.id)[:4]

    context = {
        'service': service,
        'related_services': related_services,
        'breadcrumb_items': [
            ('Home', '/'),
            ('Services', '/services/'),
            (service.name, None),
        ],
    }
    return render(request, 'products/service_page.html', context)


def services_index(request):
    services = ServicePage.objects.filter(is_published=True).order_by('display_order', 'name')
    return render(request, 'products/services_index.html', {'services': services})


# ============================================================
# BLOG
# ============================================================
def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page', 1)
    blogs_page = paginator.get_page(page_number)
    return render(request, 'products/blog_list.html', {
        'blog_posts': blogs_page,
        'current_page': int(page_number) if str(page_number).isdigit() else 1,
        'total_pages': paginator.num_pages,
    })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_published=True)
    related_blogs = Blog.objects.filter(is_published=True).exclude(id=blog.id)[:3]
    return render(request, 'products/blog_detail.html', {
        'blog': blog,
        'related_blogs': related_blogs,
        'blog_breadcrumb_items': [
            ('Home', '/'),
            ('Wall Clock Guides', '/blog/'),
            (blog.title, None),
        ],
    })


# ============================================================
# STATIC PAGES
# ============================================================
def about(request):
    site = SiteSettings.load()
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    return render(request, 'products/about.html', {
        'site': site,
        'testimonials': testimonials,
        'breadcrumb_items': [
            ('Home', '/'),
            ('About HOOVALE', None),
        ],
    })


def contact(request):
    site = SiteSettings.load()
    faqs = FAQ.objects.filter(is_active=True, scope__in=['global', 'contact'])[:6]
    return render(request, 'products/contact.html', {'site': site, 'faqs': faqs})


# ============================================================
# ROBOTS.TXT
# ============================================================
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "",
        "Sitemap: https://hoovale.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# ============================================================
# ENQUIRY (Existing — kept compatible)
# ============================================================
@csrf_exempt
@require_http_methods(["POST"])
def submit_enquiry(request):
    try:
        from enquiries.models import Enquiry
        product_id = request.POST.get('product_id')
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, phone, city, message]):
            return JsonResponse({'success': False, 'error': 'Please fill all required fields'}, status=400)

        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass

        enquiry = Enquiry.objects.create(
            product=product, name=name, phone=phone, email=email,
            city=city, message=message, status='new'
        )
        return JsonResponse({'success': True, 'message': 'Enquiry submitted!', 'enquiry_id': enquiry.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# ERROR HANDLERS
# ============================================================
def page_not_found(request, exception):
    return render(request, 'products/404.html', status=404)


def server_error(request):
    return render(request, 'products/500.html', status=500)
