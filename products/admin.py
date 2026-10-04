"""
HOOVALE Admin Configuration
Phase 1: All SEO models registered with rich admin interfaces
"""
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Category, Product, Blog, CityPage, IndustryPage,
    ServicePage, FAQ, Testimonial, Banner, SiteSettings,
    PricingTierTemplate,                                    # ← NEW
)


# ============================================================
# PRICING TIER TEMPLATE  (NEW)
# ============================================================
@admin.register(PricingTierTemplate)
class PricingTierTemplateAdmin(ModelAdmin):
    list_display  = ['name', 'tier_summary', 'product_count', 'is_active']
    list_filter   = ['is_active']
    list_editable = ['is_active']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Template', {
            'fields': ('name', 'description', 'is_active'),
            'description': (
                'Create a named pricing template and assign it to products. '
                'Name one template "Default" to apply it site-wide automatically.'
            ),
        }),
        ('Tier 1 — Sample / Trial (smallest qty)', {
            'fields': [
                ('tier1_min_qty', 'tier1_max_qty'),
                'tier1_label',
                ('tier1_discount_type', 'tier1_discount_value'),
                'tier1_badge',
            ],
        }),
        ('Tier 2 — Small Order', {
            'fields': [
                ('tier2_min_qty', 'tier2_max_qty'),
                'tier2_label',
                ('tier2_discount_type', 'tier2_discount_value'),
                'tier2_badge',
            ],
        }),
        ('Tier 3 — Standard Bulk', {
            'fields': [
                ('tier3_min_qty', 'tier3_max_qty'),
                'tier3_label',
                ('tier3_discount_type', 'tier3_discount_value'),
                'tier3_badge',
            ],
        }),
        ('Tier 4 — Large Order', {
            'fields': [
                ('tier4_min_qty', 'tier4_max_qty'),
                'tier4_label',
                ('tier4_discount_type', 'tier4_discount_value'),
                'tier4_badge',
            ],
        }),
        ('Tier 5 — Wholesale / OEM (best price)', {
            'fields': [
                ('tier5_min_qty', 'tier5_max_qty'),
                'tier5_label',
                ('tier5_discount_type', 'tier5_discount_value'),
                'tier5_badge',
            ],
            'description': 'Set max_qty to 99999 for open-ended "500+ pieces".',
        }),
    )

    def tier_summary(self, obj):
        """Shows a compact 5-tier discount summary in the list view."""
        def fmt(dv, dt):
            return f"{int(dv)}%" if dt == 'percent' else f"₹{int(dv)}"

        tiers = [
            (obj.tier1_min_qty, obj.tier1_discount_value, obj.tier1_discount_type),
            (obj.tier2_min_qty, obj.tier2_discount_value, obj.tier2_discount_type),
            (obj.tier3_min_qty, obj.tier3_discount_value, obj.tier3_discount_type),
            (obj.tier4_min_qty, obj.tier4_discount_value, obj.tier4_discount_type),
            (obj.tier5_min_qty, obj.tier5_discount_value, obj.tier5_discount_type),
        ]
        parts = [
            f'<span style="background:#f0f4ff;border-radius:3px;padding:1px 5px;font-size:0.72rem;margin-right:2px;">'
            f'{min_q}+ → {fmt(dv, dt)}</span>'
            for min_q, dv, dt in tiers
        ]
        return format_html(''.join(parts))
    tier_summary.short_description = 'Tier discounts'

    def product_count(self, obj):
        count = obj.products.count()
        color = '#0051A3' if count else '#999'
        return format_html(
            '<strong style="color:{};">{} product{}</strong>',
            color, count, 's' if count != 1 else ''
        )
    product_count.short_description = 'Assigned to'


# ============================================================
# CATEGORY
# ============================================================
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'product_count', 'is_featured', 'display_order']
    list_filter = ['is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'display_order']
    fieldsets = (
        ('Basic', {'fields': ('name', 'slug', 'description', 'image', 'static_image_path')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords', 'h1_heading', 'seo_content'),
                 'classes': ('collapse',)}),
        ('Display', {'fields': ('is_featured', 'display_order')}),
    )

    def product_count(self, obj):
        return format_html('<strong style="color:#0051A3;">{} products</strong>', obj.products.count())
    product_count.short_description = 'Products'


# ============================================================
# PRODUCT
# ============================================================
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'category', 'price', 'moq', 'tier_template_tag', 'badges', 'is_active']
    list_filter = ['category', 'is_featured', 'is_bestseller', 'is_new_arrival', 'is_active']
    search_fields = ['name', 'description', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    fieldsets = (
        ('Basic', {'fields': ('name', 'slug', 'category', 'short_description', 'description', 'specifications')}),
        ('Pricing', {'fields': ('price', 'bulk_price', 'moq')}),
        ('Wholesale Pricing Tiers', {                           # ← NEW fieldset
            'fields': ('pricing_tier_template', 'use_custom_tiers', 'custom_pricing_tiers'),
            'description': (
                '<strong>How it works:</strong> '
                'Select a template for standard tier pricing, or tick "Use custom tiers" '
                'and paste a JSON array to override for this product only. '
                'Leave both blank to use the site-wide "Default" template (or the built-in fallback). '
                '<br><br>'
                '<strong>Custom JSON format:</strong><br>'
                '<code>'
                '[{"tier":1,"min_qty":1,"max_qty":49,"label":"Sample","discount_type":"percent","discount_value":0,"badge":"MRP"},'
                ' {"tier":2,"min_qty":50,"max_qty":99,"label":"Small Order","discount_type":"percent","discount_value":5,"badge":"5% OFF"},'
                ' ...]'
                '</code><br>'
                'discount_type: <code>"percent"</code> (% off) or <code>"flat"</code> (₹ off per piece)'
            ),
            'classes': ('collapse',),
        }),
        ('Images', {'fields': ('image', 'additional_images')}),
        ('Customization', {'fields': ('size_options', 'material_options', 'color_options'),
                          'classes': ('collapse',)}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords', 'sku', 'brand', 'availability'),
                 'classes': ('collapse',)}),
        ('Open Graph', {'fields': ('og_title', 'og_description', 'og_image'),
                       'classes': ('collapse',)}),
        ('Display Flags', {'fields': ('is_featured', 'is_bestseller', 'is_new_arrival', 'is_active')}),
    )

    def badges(self, obj):
        b = []
        if obj.is_featured:    b.append('<span style="background:#FFA500;color:white;padding:2px 6px;border-radius:3px;font-size:0.7rem;">⭐ FEATURED</span>')
        if obj.is_bestseller:  b.append('<span style="background:#10b981;color:white;padding:2px 6px;border-radius:3px;font-size:0.7rem;">🔥 BESTSELLER</span>')
        if obj.is_new_arrival: b.append('<span style="background:#3b82f6;color:white;padding:2px 6px;border-radius:3px;font-size:0.7rem;">🆕 NEW</span>')
        return format_html("{}", mark_safe(" ".join(b))) if b else '-'

    def tier_template_tag(self, obj):                          # ← NEW list column
        if not hasattr(obj, 'pricing_tier_template'):
            return format_html('<span style="color:#ccc;font-size:0.75rem;">{}</span>', '—')
        if obj.use_custom_tiers and obj.custom_pricing_tiers:
            return format_html(
                '<span style="background:#fde8ff;color:#7e22ce;padding:2px 6px;'
                'border-radius:3px;font-size:0.72rem;">{}</span>',
                '✏️ Custom'
            )
        if obj.pricing_tier_template:
            return format_html(
                '<span style="background:#e8f2ff;color:#0051A3;padding:2px 6px;'
                'border-radius:3px;font-size:0.72rem;">📋 {}</span>',
                obj.pricing_tier_template.name
            )
        return format_html(
            '<span style="background:#f1f1f1;color:#666;padding:2px 6px;'
            'border-radius:3px;font-size:0.72rem;">{}</span>',
            '↩ Default'
        )
    tier_template_tag.short_description = 'Tier pricing'


# ============================================================
# CITY LANDING PAGE
# ============================================================
@admin.register(CityPage)
class CityPageAdmin(ModelAdmin):
    list_display = ['city_name', 'page_type', 'is_published', 'display_order']
    list_filter = ['page_type', 'is_published']
    search_fields = ['city_name', 'state', 'h1_heading']
    prepopulated_fields = {'slug': ('city_name',)}
    list_editable = ['is_published', 'display_order']
    fieldsets = (
        ('🏙️ City Identity', {
            'fields': ('city_name', 'slug', 'state', 'page_type'),
            'description': 'Each city = 1 SEO landing page. Add 8+ cities for maximum coverage.',
        }),
        ('🎯 Hero Section', {
            'fields': ('h1_heading', 'hero_subheading', 'hero_image'),
        }),
        ('📝 Content Sections (Total ~1500 words for ranking)', {
            'fields': ('intro_content', 'why_choose_content', 'services_content',
                      'delivery_content', 'industries_content', 'closing_content'),
            'description': 'Each section ~150-300 words. Use natural, helpful language with city name.',
        }),
        ('🔍 SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'nearby_areas', 'delivery_time'),
        }),
        ('⚙️ Display', {
            'fields': ('is_published', 'display_order'),
        }),
    )


# ============================================================
# INDUSTRY PAGE
# ============================================================
@admin.register(IndustryPage)
class IndustryPageAdmin(ModelAdmin):
    list_display = ['industry_name', 'is_published', 'display_order']
    list_filter = ['is_published']
    search_fields = ['industry_name', 'h1_heading']
    prepopulated_fields = {'slug': ('industry_name',)}
    list_editable = ['is_published', 'display_order']
    filter_horizontal = ['featured_products']


# ============================================================
# SERVICE PAGE
# ============================================================
@admin.register(ServicePage)
class ServicePageAdmin(ModelAdmin):
    list_display = ['name', 'is_published', 'display_order']
    list_filter = ['is_published']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_published', 'display_order']


# ============================================================
# FAQ
# ============================================================
@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ['question_short', 'scope', 'display_order', 'is_active']
    list_filter = ['scope', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['scope', 'display_order', 'is_active']

    def question_short(self, obj):
        return obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
    question_short.short_description = 'Question'


# ============================================================
# TESTIMONIAL
# ============================================================
@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ['customer_name', 'customer_designation', 'stars', 'is_featured', 'is_active']
    list_filter = ['rating', 'is_featured', 'is_active']
    search_fields = ['customer_name', 'review_content']
    list_editable = ['is_featured', 'is_active']

    def stars(self, obj):
        return format_html('<span style="color:#FFA500;">{}</span>', '★' * obj.rating)


# ============================================================
# BANNER (Homepage Carousel)
# ============================================================
@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'is_page_published', 'preview']
    list_filter = ['is_active', 'is_page_published']
    search_fields = ['title', 'heading', 'page_heading']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_active', 'is_page_published']
    filter_horizontal = ['page_products']
    fieldsets = (
        ('🎯 Banner Identity', {
            'fields': ('title', 'slug', 'order', 'is_active'),
        }),
        ('🖼️ Responsive Images', {
            'fields': ('desktop_image', 'mobile_image', 'image', 'fallback_desktop', 'fallback_mobile'),
            'description': (
                'Upload BOTH desktop and mobile artwork for the SAME campaign. '
                'Recommended ratio is exactly 3:2 to match the homepage carousel. '
                'Example: desktop 1200×800 and mobile 1080×720. '
                'The mobile file is shown automatically on phones; desktop is shown on larger screens.'
            ),
        }),
        ('🏷️ Homepage Slide', {
            'fields': ('heading', 'subheading', 'cta_text', 'cta_url', 'text_color', 'text_position', 'overlay_opacity'),
        }),
        ('📄 Dynamic Campaign Page', {
            'fields': (
                'page_heading', 'page_subheading', 'page_intro', 'page_content',
                'page_image', 'page_products', 'is_page_published',
                'seo_title', 'seo_description', 'seo_keywords',
            ),
            'description': (
                'The banner opens /collection/<slug>/. Select only the products '
                'that belong to this campaign. If none are selected, the page uses a general product fallback.'
            ),
        }),
    )

    def preview(self, obj):
        desktop = obj.homepage_desktop_url
        mobile = obj.homepage_mobile_url
        return format_html(
            '<div style="display:flex;gap:8px;align-items:center;">'
            '<img src="{}" title="Desktop" style="width:120px;height:80px;object-fit:cover;border-radius:8px;">'
            '<img src="{}" title="Mobile" style="width:108px;height:72px;object-fit:cover;border-radius:8px;">'
            '</div>',
            desktop, mobile
        )


# ============================================================
# SITE SETTINGS (Singleton — only 1 record)
# ============================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('Business Identity', {
            'fields': ('business_name', 'tagline', 'establishment_year', 'employee_count', 'gst_number'),
        }),
        ('Contact (CRITICAL — appears everywhere)', {
            'fields': ('primary_phone', 'whatsapp_number', 'email'),
            'description': 'These are used in sticky CTAs, footer, schema markup. WhatsApp format: 91XXXXXXXXXX',
        }),
        ('Address (LocalBusiness Schema)', {
            'fields': ('street_address', 'locality', 'region', 'postal_code', 'country', 'latitude', 'longitude'),
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'linkedin_url'),
            'classes': ('collapse',),
        }),
        ('Default SEO', {
            'fields': ('default_meta_title', 'default_meta_description'),
        }),
        ('Search Engine Verification', {
            'fields': ('google_verification', 'bing_verification'),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ============================================================
# BLOG
# ============================================================
@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'created_at']
    list_filter = ['category', 'is_published']
    search_fields = ['title', 'description', 'content_html']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    fieldsets = (
        ('Article', {'fields': ('title', 'slug', 'category', 'description', 'content_html', 'featured_image')}),
        ('Inline Images', {
            'fields': (
                'inline_image_1', 'inline_image_1_caption',
                'inline_image_2', 'inline_image_2_caption',
                'inline_image_3', 'inline_image_3_caption',
            ),
            'description': 'Image 1 appears after the article introduction, Image 2 in the middle of the guide, and Image 3 near the end. Use original, relevant product/process photos with descriptive captions.',
        }),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords')}),
        ('Publishing', {'fields': ('is_published',)}),
    )


# ============================================================
# Customize admin site
# ============================================================
admin.site.site_header = "🕐 HOOVALE Admin"
admin.site.site_title = "HOOVALE - Wall Clock Manufacturer"
admin.site.index_title = "SEO + Content Management"


# ============================================================
# AUTHENTICATION — styled user/group management
# ============================================================
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
