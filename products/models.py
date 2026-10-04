"""
HOOVALE Wall Clock Manufacturer - SEO-Optimized Models
Phase 1: SEO Foundation
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.core.validators import MinValueValidator, MaxValueValidator
import json


# ============================================================
# 1. CATEGORY (Existing - enhanced)
# ============================================================
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    static_image_path = models.CharField(max_length=300, blank=True, help_text="Optional static fallback image path, e.g. /static/images/categories/home-decor.svg")

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    h1_heading = models.CharField(max_length=200, blank=True, help_text="If empty, uses category name")
    seo_content = models.TextField(blank=True, help_text="800+ word SEO content for category page")

    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} Manufacturer & Supplier in Jaipur | HOOVALE"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_products', kwargs={'slug': self.slug})




# ============================================================
# PRICING TIER TEMPLATE (Global Default Templates)
# ============================================================
# Admins create named templates here (e.g. "Standard Wall Clocks",
# "Premium Clocks", "Budget Range") and assign them to products.
# Each product can also override with its own custom tiers.

class PricingTierTemplate(models.Model):
    """
    Reusable pricing tier templates manageable from Django Admin.
    
    Each template defines 5 quantity bands (Tier 1–5).
    Discount can be set as PERCENT OFF or FLAT RUPEES OFF per piece.
    
    Admin flow:
      1. Create a template (e.g. "Standard — 5 slabs")
      2. Set 5 tier rows: min_qty, max_qty, discount_type, discount_value
      3. Assign to products via product.pricing_tier_template FK
      4. Products can still override with product.custom_pricing_tiers JSON
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Admin label, e.g. 'Standard 5-tier', 'Premium Clocks', 'Budget Range'"
    )
    description = models.CharField(max_length=300, blank=True)

    # ── Tier 1 (smallest qty) ─────────────────────────────
    tier1_min_qty = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)],
        help_text="Minimum order quantity for Tier 1"
    )
    tier1_max_qty = models.PositiveIntegerField(
        default=49,
        help_text="Maximum qty for Tier 1 (use 99999 for 'no upper limit')"
    )
    tier1_label = models.CharField(
        max_length=50, default='Sample / Trial',
        help_text="Display label, e.g. 'Sample / Trial'"
    )
    DISCOUNT_TYPE_CHOICES = [
        ('percent', '% Off per piece'),
        ('flat', '₹ Off per piece'),
    ]
    tier1_discount_type = models.CharField(
        max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent'
    )
    tier1_discount_value = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        help_text="If type=percent: 0–100. If type=flat: rupees off per piece"
    )
    tier1_badge = models.CharField(
        max_length=30, blank=True,
        help_text="Optional badge text, e.g. 'MRP', 'Trial Price'"
    )

    # ── Tier 2 ────────────────────────────────────────────
    tier2_min_qty = models.PositiveIntegerField(default=50)
    tier2_max_qty = models.PositiveIntegerField(default=99)
    tier2_label = models.CharField(max_length=50, default='Small Order')
    tier2_discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent')
    tier2_discount_value = models.DecimalField(max_digits=8, decimal_places=2, default=5)
    tier2_badge = models.CharField(max_length=30, blank=True, default='5% OFF')

    # ── Tier 3 ────────────────────────────────────────────
    tier3_min_qty = models.PositiveIntegerField(default=100)
    tier3_max_qty = models.PositiveIntegerField(default=249)
    tier3_label = models.CharField(max_length=50, default='Standard Bulk')
    tier3_discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent')
    tier3_discount_value = models.DecimalField(max_digits=8, decimal_places=2, default=10)
    tier3_badge = models.CharField(max_length=30, blank=True, default='10% OFF')

    # ── Tier 4 ────────────────────────────────────────────
    tier4_min_qty = models.PositiveIntegerField(default=250)
    tier4_max_qty = models.PositiveIntegerField(default=499)
    tier4_label = models.CharField(max_length=50, default='Large Order')
    tier4_discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent')
    tier4_discount_value = models.DecimalField(max_digits=8, decimal_places=2, default=15)
    tier4_badge = models.CharField(max_length=30, blank=True, default='15% OFF')

    # ── Tier 5 (biggest qty) ──────────────────────────────
    tier5_min_qty = models.PositiveIntegerField(default=500)
    tier5_max_qty = models.PositiveIntegerField(
        default=99999,
        help_text="Set 99999 for open-ended (500+)"
    )
    tier5_label = models.CharField(max_length=50, default='Wholesale / OEM')
    tier5_discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent')
    tier5_discount_value = models.DecimalField(max_digits=8, decimal_places=2, default=20)
    tier5_badge = models.CharField(max_length=30, blank=True, default='Best Price 🏆')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Pricing Tier Template'
        verbose_name_plural = 'Pricing Tier Templates'

    def __str__(self):
        return self.name

    def as_tiers_list(self):
        """
        Returns structured list of 5 tiers for use in templates/JS.
        Each tier: {min_qty, max_qty, label, discount_type, discount_value, badge}
        """
        return [
            {
                'tier': i + 1,
                'min_qty': getattr(self, f'tier{i+1}_min_qty'),
                'max_qty': getattr(self, f'tier{i+1}_max_qty'),
                'label': getattr(self, f'tier{i+1}_label'),
                'discount_type': getattr(self, f'tier{i+1}_discount_type'),
                'discount_value': float(getattr(self, f'tier{i+1}_discount_value')),
                'badge': getattr(self, f'tier{i+1}_badge'),
            }
            for i in range(5)
        ]





# ============================================================
# 2. PRODUCT (Existing - enhanced for SEO)
# ============================================================
class Product(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    # Content
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    specifications = models.TextField(blank=True, help_text="One per line: 'Key: Value'")

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    bulk_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                     help_text="Discounted price for bulk orders")
    moq = models.PositiveIntegerField(default=1, help_text="Minimum Order Quantity")

    # Wholesale Pricing Tiers                                  # ← NEW
    pricing_tier_template = models.ForeignKey(               # ← NEW
        'PricingTierTemplate',                                # ← NEW
        on_delete=models.SET_NULL,                            # ← NEW
        null=True, blank=True,                                # ← NEW
        related_name='products',                              # ← NEW
        help_text="Select a reusable pricing template. Leave blank to use site default.",  # ← NEW
    )                                                         # ← NEW
    custom_pricing_tiers = models.JSONField(                  # ← NEW
        blank=True, null=True,                                # ← NEW
        help_text=(                                           # ← NEW
            "Override tiers for this product only. Leave blank to use the template. "  # ← NEW
            "Format: list of 5 dicts with keys: "            # ← NEW
            "min_qty, max_qty, label, discount_type (percent/flat), discount_value, badge."  # ← NEW
        ),                                                    # ← NEW
    )                                                         # ← NEW
    use_custom_tiers = models.BooleanField(                   # ← NEW
        default=False,                                        # ← NEW
        help_text="Tick to use the custom tiers JSON above instead of the template.",  # ← NEW
    )                                                         # ← NEW

    # Images
    image = models.ImageField(upload_to='products/')
    additional_images = models.JSONField(default=list, blank=True)

    # Customization
    size_options = models.JSONField(default=list, blank=True)
    material_options = models.JSONField(default=list, blank=True)
    color_options = models.JSONField(default=list, blank=True)

    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    # Open Graph
    og_title = models.CharField(max_length=100, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to='og_images/', blank=True, null=True)

    # Schema.org product fields
    brand = models.CharField(max_length=100, default='HOOVALE')
    sku = models.CharField(max_length=50, blank=True)
    availability = models.CharField(max_length=30, default='InStock',
                                   choices=[('InStock','In Stock'),('OutOfStock','Out of Stock'),('PreOrder','Pre Order')])

    # Display flags
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Always keep the public slug unique so adding a product with an
        # existing/similar name cannot turn a normal admin save into HTTP 500.
        base_slug = slugify(self.slug or self.name) or "product"
        candidate = base_slug
        counter = 2
        while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
            candidate = f"{base_slug}-{counter}"
            counter += 1
        self.slug = candidate

        if not self.meta_title:
            # meta_title is limited to 70 characters in the database.
            # Product names can be much longer, so never generate a value
            # that can exceed the database column size.
            generated_title = f"{self.name} | Wholesale Wall Clock Manufacturer Jaipur"
            self.meta_title = generated_title[:70].rstrip()
        else:
            # Keep programmatic/admin saves safe even when a value is supplied
            # outside Django form validation.
            self.meta_title = self.meta_title[:70].rstrip()

        if not self.meta_description:
            clean = strip_tags(self.description)[:155]
            self.meta_description = f"{clean}..."[:160]
        else:
            self.meta_description = self.meta_description[:160].rstrip()
        if not self.sku:
            self.sku = f"HV-{self.id or 'NEW'}-{slugify(self.name)[:10].upper()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        """Return a safe product image URL without ever raising on a blank ImageField."""
        try:
            if self.image:
                return self.image.url
        except (ValueError, AttributeError):
            pass
        return '/static/images/product-placeholder.svg'

    # ── Pricing Tier Methods ──────────────────────────────── # ← NEW
    def get_pricing_tiers(self):                              # ← NEW
        """
        Returns the resolved 5-tier pricing list for this product.

        Priority order:
          1. product.custom_pricing_tiers  (if use_custom_tiers=True)
          2. product.pricing_tier_template (assigned template)
          3. PricingTierTemplate(name='Default')  (site-wide default)
          4. Hard-coded fallback  (always works, no DB or migration needed)
        """
        # 1. Product-level custom override
        if self.use_custom_tiers and self.custom_pricing_tiers:
            return self.custom_pricing_tiers

        # 2. Assigned template
        if self.pricing_tier_template_id:
            try:
                return self.pricing_tier_template.as_tiers_list()
            except Exception:
                pass

        # 3. Site-wide default template
        try:
            from django.apps import apps
            PricingTierTemplate = apps.get_model(
                self._meta.app_label, 'PricingTierTemplate'
            )
            default = PricingTierTemplate.objects.filter(
                is_active=True, name='Default'
            ).first()
            if default:
                return default.as_tiers_list()
        except Exception:
            pass

        # 4. Hard-coded fallback — zero config needed
        return [
            {'tier': 1, 'min_qty': 1,   'max_qty': 49,    'label': 'Sample / Trial', 'discount_type': 'percent', 'discount_value': 0,  'badge': 'MRP'},
            {'tier': 2, 'min_qty': 50,  'max_qty': 99,    'label': 'Small Order',    'discount_type': 'percent', 'discount_value': 5,  'badge': '5% OFF'},
            {'tier': 3, 'min_qty': 100, 'max_qty': 249,   'label': 'Standard Bulk',  'discount_type': 'percent', 'discount_value': 10, 'badge': '10% OFF'},
            {'tier': 4, 'min_qty': 250, 'max_qty': 499,   'label': 'Large Order',    'discount_type': 'percent', 'discount_value': 15, 'badge': '15% OFF'},
            {'tier': 5, 'min_qty': 500, 'max_qty': 99999, 'label': 'Wholesale / OEM','discount_type': 'percent', 'discount_value': 22, 'badge': 'Best Price'},
        ]

    def get_price_for_qty(self, qty):                        # ← NEW
        """
        Returns a dict with computed pricing for a given quantity.
        Useful in views, APIs, or the Django shell for quick checks.

        Example:
            product.get_price_for_qty(150)
            → {'unit_price': 405.0, 'total_price': 60750.0,
               'saving_per_piece': 45.0, 'total_saving': 6750.0,
               'tier': {...}}
        """
        base = float(self.price or 0)
        tiers = self.get_pricing_tiers()

        active_tier = tiers[0]
        for t in tiers:
            if t['min_qty'] <= qty <= t['max_qty']:
                active_tier = t
                break

        dv = float(active_tier.get('discount_value', 0))
        if active_tier.get('discount_type') == 'percent':
            saving = base * dv / 100
        else:
            saving = dv

        unit_price = max(0, base - saving)
        return {
            'unit_price':     round(unit_price, 2),
            'total_price':    round(unit_price * qty, 2),
            'saving_per_piece': round(saving, 2),
            'total_saving':   round(saving * qty, 2),
            'tier':           active_tier,
        }

# ============================================================
# 3. CITY LANDING PAGE (NEW — Programmatic SEO)
# ============================================================
class CityPage(models.Model):
    """
    One model = unlimited city landing pages.
    URL: /wall-clock-supplier-in-{city-slug}/
    """
    city_name = models.CharField(max_length=100, unique=True, help_text="e.g., Delhi, Mumbai, Bangalore")
    slug = models.SlugField(unique=True, blank=True, help_text="Auto-generated from city name")
    state = models.CharField(max_length=100, blank=True)

    # Page type (controls URL pattern + content tone)
    PAGE_TYPE_CHOICES = [
        ('manufacturer', 'Manufacturer in [City]'),
        ('supplier', 'Supplier in [City]'),
        ('wholesaler', 'Wholesaler in [City]'),
    ]
    page_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES, default='supplier')

    # Hero section
    h1_heading = models.CharField(max_length=200, help_text="e.g., 'Wall Clock Supplier in Delhi'")
    hero_subheading = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='city_pages/', blank=True, null=True)

    # Content (each section ~150-300 words for ~1500 word total page)
    intro_content = models.TextField(help_text="Opening section: who you serve in this city")
    why_choose_content = models.TextField(blank=True, help_text="Why choose HOOVALE for this city")
    services_content = models.TextField(blank=True, help_text="Services offered to this city")
    delivery_content = models.TextField(blank=True, help_text="Delivery info to this city")
    industries_content = models.TextField(blank=True, help_text="Industries served in this city")
    closing_content = models.TextField(blank=True, help_text="Final CTA paragraph")

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=400, blank=True,
                                    help_text="Comma-separated, e.g., 'wall clock supplier delhi, ...'")

    # Local relevance
    nearby_areas = models.TextField(blank=True, help_text="Comma-separated nearby areas/pincodes")
    delivery_time = models.CharField(max_length=50, blank=True, default='3-5 business days')

    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'city_name']
        verbose_name = 'City Landing Page'
        verbose_name_plural = 'City Landing Pages (SEO)'

    def __str__(self):
        return f"Wall Clock {self.get_page_type_display()} {self.city_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.city_name)
        if not self.meta_title:
            self.meta_title = f"Wall Clock {self.get_page_type_display().split(' in')[0]} in {self.city_name} | HOOVALE Jaipur"
        if not self.meta_description:
            self.meta_description = (
                f"Top wall clock {self.page_type} in {self.city_name}. "
                f"Bulk orders, custom logo printing, fast delivery from Jaipur. "
                f"Call/WhatsApp for wholesale prices."
            )[:160]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('city_landing', kwargs={'slug': self.slug})


# ============================================================
# 4. INDUSTRY PAGE (NEW — Vertical SEO)
# ============================================================
class IndustryPage(models.Model):
    """
    Industry-specific landing pages.
    URL: /wall-clocks-for-{industry-slug}/
    Examples: corporate offices, hotels, hospitals, schools, retail
    """
    industry_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="FontAwesome class, e.g., 'fa-building'")

    # Hero
    h1_heading = models.CharField(max_length=200)
    hero_subheading = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='industries/', blank=True, null=True)

    # Content
    intro_content = models.TextField()
    benefits_content = models.TextField(blank=True)
    customization_content = models.TextField(blank=True)
    case_study_content = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=400, blank=True)

    # Recommended products (M2M to Product)
    featured_products = models.ManyToManyField(Product, blank=True, related_name='industries')

    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'industry_name']
        verbose_name_plural = 'Industry Pages (SEO)'

    def __str__(self):
        return self.industry_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.industry_name)
        if not self.meta_title:
            self.meta_title = f"Wall Clocks for {self.industry_name} | Bulk Supplier | HOOVALE"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('industry_page', kwargs={'slug': self.slug})


# ============================================================
# 5. FAQ (NEW — for FAQ schema markup)
# ============================================================
class FAQ(models.Model):
    """
    Site-wide and page-specific FAQs.
    Renders as schema.org FAQPage markup → rich snippets in Google.
    """
    question = models.CharField(max_length=300)
    answer = models.TextField()

    # Where to display
    SCOPE_CHOICES = [
        ('global', 'Global (All Pages)'),
        ('home', 'Homepage Only'),
        ('product', 'Product Pages'),
        ('city', 'City Pages'),
        ('industry', 'Industry Pages'),
        ('contact', 'Contact Page'),
        ('about', 'About Page'),
    ]
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='global')

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scope', 'display_order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


# ============================================================
# 6. TESTIMONIAL (NEW — for Review schema)
# ============================================================
class Testimonial(models.Model):
    """Customer testimonials. Renders as schema.org Review markup."""
    customer_name = models.CharField(max_length=200)
    customer_designation = models.CharField(max_length=200, blank=True,
                                          help_text="e.g., 'Purchase Manager, ABC Hotels'")
    customer_city = models.CharField(max_length=100, blank=True)
    customer_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    rating = models.PositiveSmallIntegerField(default=5,
                                            choices=[(i, str(i)) for i in range(1, 6)])
    review_title = models.CharField(max_length=200, blank=True)
    review_content = models.TextField()

    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', 'display_order', '-created_at']

    def __str__(self):
        return f"{self.customer_name} ({self.rating}★)"


# ============================================================
# 7. SERVICE PAGE (NEW — OEM, Bulk, Customization etc.)
# ============================================================
class ServicePage(models.Model):
    """
    Service-specific landing pages.
    URL: /services/{slug}/
    Examples: OEM Manufacturing, Bulk Orders, Custom Logo Printing
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True)

    h1_heading = models.CharField(max_length=200)
    hero_subheading = models.CharField(max_length=300, blank=True)
    hero_image = models.ImageField(upload_to='services/', blank=True, null=True)

    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    process_content = models.TextField(blank=True, help_text="How the service works")
    benefits_content = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=400, blank=True)

    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Service Pages'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} | Wall Clock Manufacturer Jaipur | HOOVALE"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_page', kwargs={'slug': self.slug})


# ============================================================
# 8. BANNER (NEW — Homepage carousel)
# ============================================================
class Banner(models.Model):
    """Marketplace banner + dynamic campaign landing page."""
    BANNER_TYPE_CHOICES = [
        ('website', '💻 Desktop / Website Banner'),
        ('mobile', '📱 Mobile Banner'),
    ]

    title = models.CharField(max_length=200, help_text="Internal/admin banner name")
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    # Legacy single-image field kept for existing records.
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPE_CHOICES, default='website')
    image = models.ImageField(upload_to='banners/', blank=True, null=True)

    # Recommended: upload both sizes on ONE banner.
    desktop_image = models.ImageField(
        upload_to='banners/desktop/', blank=True, null=True,
        help_text="Recommended 1200×800 (or 1440×960), exact 3:2 ratio for the homepage carousel card."
    )
    mobile_image = models.ImageField(
        upload_to='banners/mobile/', blank=True, null=True,
        help_text="Recommended 1200×800 (or 1080×720), exact 3:2 ratio for the homepage carousel card; use the same ratio on mobile."
    )
    fallback_desktop = models.CharField(
        max_length=300, blank=True,
        help_text="Optional static fallback path, e.g. /static/images/banners/wedding-desktop.svg"
    )
    fallback_mobile = models.CharField(
        max_length=300, blank=True,
        help_text="Optional static fallback path for mobile."
    )

    # Homepage slide copy.
    heading = models.CharField(max_length=200, blank=True)
    subheading = models.CharField(max_length=400, blank=True)
    cta_text = models.CharField(max_length=100, blank=True, default='Explore')
    cta_url = models.CharField(max_length=500, blank=True, default='')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Dynamic landing page opened when the banner is clicked.
    page_heading = models.CharField(max_length=220, blank=True)
    page_subheading = models.CharField(max_length=400, blank=True)
    page_intro = models.TextField(blank=True)
    page_content = models.TextField(
        blank=True,
        help_text="Main campaign content. Keep it useful and specific to the banner."
    )
    page_image = models.ImageField(upload_to='banner_pages/', blank=True, null=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    seo_keywords = models.CharField(max_length=400, blank=True)
    page_products = models.ManyToManyField(
        'Product', blank=True, related_name='campaign_banners',
        help_text="Only selected products appear on this campaign page."
    )
    is_page_published = models.BooleanField(default=True)

    text_color = models.CharField(max_length=7, default='#FFFFFF')
    text_position = models.CharField(max_length=20, default='center-center', choices=[
        ('top-left','Top Left'),('top-center','Top Center'),('top-right','Top Right'),
        ('center-left','Center Left'),('center-center','Center'),('center-right','Center Right'),
        ('bottom-left','Bottom Left'),('bottom-center','Bottom Center'),('bottom-right','Bottom Right'),
    ])
    overlay_opacity = models.FloatField(default=0.4, help_text="0.0 (clear) to 1.0 (black)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Homepage / Campaign Banner'
        verbose_name_plural = 'Homepage / Campaign Banners'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('banner_page', kwargs={'slug': self.slug})

    @property
    def homepage_desktop_url(self):
        if self.desktop_image:
            return self.desktop_image.url
        if self.image and self.banner_type == 'website':
            return self.image.url
        return self.fallback_desktop or '/static/images/banners/default-desktop.svg'

    @property
    def homepage_mobile_url(self):
        if self.mobile_image:
            return self.mobile_image.url
        if self.image and self.banner_type == 'mobile':
            return self.image.url
        return self.fallback_mobile or self.fallback_desktop or '/static/images/banners/default-mobile.svg'


# ============================================================
# 9. SITE SETTINGS (NEW — Centralized config)
# ============================================================
class SiteSettings(models.Model):
    """
    Singleton model for site-wide settings.
    Phone number, WhatsApp number, address, etc. all editable from admin.
    """
    # Business identity
    business_name = models.CharField(max_length=200, default='HOOVALE')
    tagline = models.CharField(max_length=300, default='Premium Wall Clock Manufacturer in Jaipur')

    # Contact
    primary_phone = models.CharField(max_length=20, default='+919462207356')
    whatsapp_number = models.CharField(max_length=20, default='919462207356',
                                      help_text="Format: 91XXXXXXXXXX (no + or -)")
    email = models.EmailField(default='info@hoovale.com')

    # Address (for LocalBusiness schema)
    street_address = models.CharField(max_length=300, default='Jaipur, Rajasthan, India')
    locality = models.CharField(max_length=100, default='Jaipur')
    region = models.CharField(max_length=100, default='Rajasthan')
    postal_code = models.CharField(max_length=10, default='302001')
    country = models.CharField(max_length=10, default='IN')

    # Geo coordinates for LocalBusiness schema
    latitude = models.FloatField(default=26.9124)
    longitude = models.FloatField(default=75.7873)

    # Business credentials (EEAT signals)
    gst_number = models.CharField(max_length=20, blank=True, help_text="GST Number for trust")
    establishment_year = models.PositiveIntegerField(default=2010)
    employee_count = models.CharField(max_length=20, blank=True, default='10-50')

    # Social
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # SEO defaults
    default_meta_title = models.CharField(max_length=70,
        default='HOOVALE — Wall Clock Manufacturer & Supplier in Jaipur')
    default_meta_description = models.CharField(max_length=160,
        default='Leading wall clock manufacturer in Jaipur. Bulk orders, custom logo printing, OEM supply across India. Call for wholesale prices.')

    # Verification
    google_verification = models.CharField(max_length=200, blank=True)
    bing_verification = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ============================================================
# 10. BLOG (Existing — kept compatible)
# ============================================================
class Blog(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=100, default='Wall Clocks')
    featured_image = models.ImageField(
    upload_to='blog/%Y/%m/',
    blank=True,
    null=True,
    default='default/blog-default.jpg'
)
    description = models.TextField(help_text="Short/plain-text summary for listings and SEO")
    content_html = models.TextField(blank=True, help_text="Optional article body HTML. Use headings, lists and links; keep content useful for readers.")
    inline_image_1 = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)
    inline_image_2 = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)
    inline_image_3 = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)
    inline_image_1_caption = models.CharField(max_length=180, blank=True)
    inline_image_2_caption = models.CharField(max_length=180, blank=True)
    inline_image_3_caption = models.CharField(max_length=180, blank=True)

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
