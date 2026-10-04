from django.db import migrations, models
from django.utils.text import slugify
import django.db.models.deletion



def backfill_banner_slugs(apps, schema_editor):
    Banner = apps.get_model('products', 'Banner')
    used = set()
    for banner in Banner.objects.all().order_by('id'):
        base = slugify(banner.title) or f'banner-{banner.id}'
        slug = base
        n = 2
        while slug in used or Banner.objects.filter(slug=slug).exclude(pk=banner.pk).exists():
            slug = f'{base}-{n}'
            n += 1
        banner.slug = slug
        banner.save(update_fields=['slug'])
        used.add(slug)


def backfill_banner_optional_fields(apps, schema_editor):
    Banner = apps.get_model('products', 'Banner')
    for banner in Banner.objects.all():
        changed = False
        for field in (
            'page_heading', 'page_subheading', 'page_intro', 'page_content',
            'seo_title', 'seo_description', 'seo_keywords',
            'fallback_desktop', 'fallback_mobile',
        ):
            if getattr(banner, field, None) is None:
                setattr(banner, field, '')
                changed = True
        if changed:
            banner.save()


def seed_hoovale_catalog(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')
    Banner = apps.get_model('products', 'Banner')

    categories = [
        {
            'name': 'Home & Decorative Wall Clocks',
            'slug': 'home-decorative-wall-clocks',
            'description': 'Wall clocks for home, office and everyday decoration, including round analog designs and decorative styles.',
            'meta_title': 'Home & Decorative Wall Clocks | HOOVALE Jaipur',
            'meta_description': 'Explore HOOVALE wall clocks for home, office and decoration, with bulk and retail enquiry support from Jaipur.',
            'meta_keywords': 'home wall clock, decorative wall clock, wall clock Jaipur, round wall clock',
            'h1_heading': 'Home & Decorative Wall Clocks',
            'static_image_path': '/static/images/categories/home-decor.svg',
            'is_featured': True, 'display_order': 1,
        },
        {
            'name': 'Wooden Wall Clocks',
            'slug': 'wooden-wall-clocks',
            'description': 'Wooden wall clocks for home and office decoration, with round designs and gifting use.',
            'meta_title': 'Wooden Wall Clocks Manufacturer in Jaipur | HOOVALE',
            'meta_description': 'Wooden wall clocks for home, office and gifting. Explore HOOVALE Jaipur supply and request current wholesale pricing.',
            'meta_keywords': 'wooden wall clocks Jaipur, wooden clock supplier, wooden wall clock wholesale',
            'h1_heading': 'Wooden Wall Clocks',
            'static_image_path': '/static/images/categories/wooden.svg',
            'is_featured': True, 'display_order': 2,
        },
        {
            'name': 'Customized & Photo Printed Clocks',
            'slug': 'customized-photo-printed-clocks',
            'description': 'Customized wall clocks for logo, photo, text and campaign artwork requirements, subject to design approval.',
            'meta_title': 'Customized Wall Clocks in Jaipur | Logo & Photo Printing | HOOVALE',
            'meta_description': 'Customized wall clocks for logo, photo and branding requirements. Share artwork and quantity for a current HOOVALE quote.',
            'meta_keywords': 'customized wall clock Jaipur, photo printed clock, personalized wall clock, logo clock',
            'h1_heading': 'Customized & Photo Printed Clocks',
            'static_image_path': '/static/images/categories/custom.svg',
            'is_featured': True, 'display_order': 3,
        },
        {
            'name': 'Corporate & Logo Wall Clocks',
            'slug': 'corporate-logo-wall-clocks',
            'description': 'Logo and corporate promotional wall clocks for offices, business gifting and brand visibility requirements.',
            'meta_title': 'Corporate Logo Wall Clocks | Bulk Supplier Jaipur | HOOVALE',
            'meta_description': 'Corporate and logo wall clocks for business gifting, office use and promotional requirements. Bulk enquiries welcome.',
            'meta_keywords': 'corporate wall clock, logo wall clock, promotional corporate clock, bulk clock',
            'h1_heading': 'Corporate & Logo Wall Clocks',
            'static_image_path': '/static/images/categories/corporate.svg',
            'is_featured': True, 'display_order': 4,
        },
        {
            'name': 'Promotional & Advertising Clocks',
            'slug': 'promotional-advertising-clocks',
            'description': 'Promotional clocks for advertising, gifting and brand campaigns, with customizable artwork and bulk quantities.',
            'meta_title': 'Promotional Wall Clocks Manufacturer Jaipur | HOOVALE',
            'meta_description': 'Promotional and advertising wall clocks for bulk branding campaigns, gifting and business promotion from Jaipur.',
            'meta_keywords': 'promotional wall clock, advertising clock, branding clock, promotional gifts Jaipur',
            'h1_heading': 'Promotional & Advertising Clocks',
            'static_image_path': '/static/images/categories/promotional.svg',
            'is_featured': True, 'display_order': 5,
        },
        {
            'name': 'Political Campaign Clocks',
            'slug': 'political-campaign-clocks',
            'description': 'Customized wall clocks for political campaign and outreach requirements, produced to approved artwork and quantity specifications.',
            'meta_title': 'Political Campaign Wall Clocks | Custom Bulk Orders | HOOVALE',
            'meta_description': 'Custom wall clocks for political campaign and outreach requirements. Share artwork, quantity and delivery city for a quote.',
            'meta_keywords': 'political campaign wall clock, political promotion clock, campaign promotional clock',
            'h1_heading': 'Political Campaign Clocks',
            'static_image_path': '/static/images/categories/political.svg',
            'is_featured': True, 'display_order': 6,
        },
        {
            'name': 'Wedding & Gifting Wall Clocks',
            'slug': 'wedding-gifting-wall-clocks',
            'description': 'Wall clocks suited to wedding, anniversary, festival and promotional gifting, with customization where available.',
            'meta_title': 'Wedding & Gifting Wall Clocks | Customized Gifts | HOOVALE',
            'meta_description': 'Wall clocks for wedding, anniversary and gifting requirements. Discuss customization, quantity and current pricing with HOOVALE.',
            'meta_keywords': 'wedding gift wall clock, anniversary clock, personalized gifting clock, return gift clock',
            'h1_heading': 'Wedding & Gifting Wall Clocks',
            'static_image_path': '/static/images/categories/wedding-gifting.svg',
            'is_featured': True, 'display_order': 7,
        },
        {
            'name': 'Office & Institutional Wall Clocks',
            'slug': 'office-institutional-wall-clocks',
            'description': 'Practical analog wall clocks for offices, schools, institutions, shops and other everyday spaces.',
            'meta_title': 'Office & Institutional Wall Clocks | HOOVALE Jaipur',
            'meta_description': 'Practical wall clocks for offices, institutions, shops and everyday spaces, with bulk supply support from Jaipur.',
            'meta_keywords': 'office wall clock, institutional wall clock, school wall clock, shop wall clock Jaipur',
            'h1_heading': 'Office & Institutional Wall Clocks',
            'static_image_path': '/static/images/categories/office-institutional.svg',
            'is_featured': True, 'display_order': 8,
        },
    ]

    cat_by_slug = {}
    for data in categories:
        defaults = dict(data)
        defaults.pop('slug')
        obj, _ = Category.objects.update_or_create(slug=data['slug'], defaults=defaults)
        cat_by_slug[data['slug']] = obj

    # These product records are based on public Hoovale Ventures listings.
    # Prices are the lower end of published ranges; the description explicitly
    # preserves the range so the site never presents a range as a fixed quote.
    products = [
        {
            'name': 'Wooden Wall Clocks',
            'slug': 'wooden-wall-clocks',
            'category': 'wooden-wall-clocks',
            'description': 'Round wooden wall clocks listed for home, office and decoration use. Public Hoovale Ventures listings describe an analog, wall-mounted design in white with gifting use for occasions such as festivals and anniversaries. Published price range: ₹145–₹178 per piece; MOQ 20 pieces. Confirm current price, finish and available variants before ordering.',
            'short_description': 'Round wooden wall clock for home, office and gifting.',
            'price': 145, 'moq': 20,
            'specifications': 'Published price range: ₹145–₹178/piece\nMOQ: 20 pieces\nShape: Round\nColor: White\nDisplay: Analog\nMounting: Wall mounted\nUsage: Home, office, decoration\nGift occasions: New Year, festival, anniversary',
            'sizes': ['Round'], 'materials': ['Wood'], 'colors': ['White'],
            'meta_title': 'Wooden Wall Clocks Manufacturer Jaipur | HOOVALE',
            'meta_description': 'Wooden wall clocks for home, office and decoration. Published range ₹145–₹178/piece with MOQ 20; confirm current quote.',
            'meta_keywords': 'wooden wall clocks Jaipur, wooden wall clock supplier, wooden clock wholesale',
            'featured': True, 'new': True, 'best': True,
        },
        {
            'name': 'Wall Clocks 10 Inch Black',
            'slug': 'wall-clocks-10-inch-black',
            'category': 'home-decorative-wall-clocks',
            'description': 'Round black plastic analog wall clock listed by Hoovale Ventures for home, office and decoration. The published listing specifies 10-inch size, round dial, wall mounting and MOQ 50 pieces. Published price range: ₹120–₹145 per piece. Confirm current availability and specifications before ordering.',
            'short_description': '10-inch black round plastic wall clock.',
            'price': 120, 'moq': 50,
            'specifications': 'Published price range: ₹120–₹145/piece\nMOQ: 50 pieces\nSize: 10 inch\nClock type: Analog\nDial shape: Round\nMaterial: Plastic\nColor: Black\nMounting: Wall mounted',
            'sizes': ['10 inch'], 'materials': ['Plastic'], 'colors': ['Black'],
            'meta_title': '10 Inch Black Wall Clock Supplier Jaipur | HOOVALE',
            'meta_description': '10-inch black round plastic wall clock. Published range ₹120–₹145/piece, MOQ 50; confirm current wholesale quote.',
            'meta_keywords': '10 inch black wall clock Jaipur, round plastic wall clock, wall clock wholesale',
            'featured': True, 'new': True, 'best': False,
        },
        {
            'name': 'Promotional Table Clock',
            'slug': 'promotional-table-clock',
            'category': 'promotional-advertising-clocks',
            'description': 'Promotional gifting clock listed by Hoovale Ventures as a modern, polished plastic battery-driven round design. The listing describes it for promotional gifts and customized poster design. Published price range: ₹95–₹135 per piece; MOQ 20 pieces. Confirm the current model and whether the requirement is wall or table format before ordering.',
            'short_description': 'Promotional gifting clock for customized artwork.',
            'price': 95, 'moq': 20,
            'specifications': 'Published price range: ₹95–₹135/piece\nMOQ: 20 pieces\nApplication: Promotional gifts\nStyle: Modern\nMaterial: Plastic\nDrive: Battery\nShape: Round\nFinish: Polished',
            'sizes': ['Round'], 'materials': ['Plastic'], 'colors': ['Custom'],
            'meta_title': 'Promotional Table Clock Supplier Jaipur | HOOVALE',
            'meta_description': 'Promotional gifting clock with customized poster design. Published range ₹95–₹135/piece; MOQ 20, subject to confirmation.',
            'meta_keywords': 'promotional table clock Jaipur, promotional gifting clock, customized clock',
            'featured': True, 'new': True, 'best': False,
        },
        {
            'name': 'Political Parties Wall Clock',
            'slug': 'political-parties-wall-clock',
            'category': 'political-campaign-clocks',
            'description': 'Round brown plastic analog wall clock listed for political party promotional requirements. The public listing specifies wall mounting, analog display and thermocol/paper box packaging. Published price range: ₹95–₹145 per piece with MOQ 20 pieces. Final artwork, quantity and current price should be confirmed before production.',
            'short_description': 'Round customized wall clock for campaign promotion.',
            'price': 95, 'moq': 20,
            'specifications': 'Published price range: ₹95–₹145/piece\nMOQ: 20 pieces\nMaterial: Plastic\nShape: Round\nColor: Brown\nDisplay: Analog\nMounting: Wall mounted\nPackaging: Thermocol / paper box',
            'sizes': ['Round'], 'materials': ['Plastic'], 'colors': ['Brown'],
            'meta_title': 'Political Campaign Wall Clock Supplier Jaipur | HOOVALE',
            'meta_description': 'Round political campaign wall clock listing from Hoovale Ventures. Published ₹95–₹145/piece, MOQ 20; confirm artwork and quote.',
            'meta_keywords': 'political campaign wall clock Jaipur, political promotion clock, campaign wall clock',
            'featured': True, 'new': False, 'best': False,
        },
        {
            'name': 'Logo Wall Clock',
            'slug': 'logo-wall-clock',
            'category': 'corporate-logo-wall-clocks',
            'description': 'Round black plastic analog logo wall clock listed by Hoovale Ventures for home, office and decoration use. The public listing specifies wall mounting and MOQ 20 pieces. Published price range: ₹90–₹150 per piece. Confirm logo artwork, print method and current price before ordering.',
            'short_description': 'Round black logo wall clock for branding.',
            'price': 90, 'moq': 20,
            'specifications': 'Published price range: ₹90–₹150/piece\nMOQ: 20 pieces\nMaterial: Plastic\nShape: Round\nColor: Black\nDisplay: Analog\nMounting: Wall mounted\nUsage: Home, office, decoration',
            'sizes': ['Round'], 'materials:': ['Plastic'], 'colors': ['Black'],
            'meta_title': 'Logo Wall Clock Manufacturer Jaipur | HOOVALE',
            'meta_description': 'Logo wall clock for home, office and branding. Published range ₹90–₹150/piece with MOQ 20; confirm current customization quote.',
            'meta_keywords': 'logo wall clock Jaipur, corporate logo clock, customized branding clock',
            'featured': True, 'new': True, 'best': True,
        },
        {
            'name': 'Customized Wall Clock',
            'slug': 'customized-wall-clock',
            'category': 'customized-photo-printed-clocks',
            'description': 'Customized round black plastic wall clock listed by Hoovale Ventures for home, office and decoration. The public listing specifies wall mounting and thermocol box packaging, with MOQ 50 pieces. Published price range: ₹110–₹145 per piece. Confirm artwork, print area and current quote.',
            'short_description': 'Customized round black wall clock for personal or business artwork.',
            'price': 110, 'moq': 50,
            'specifications': 'Published price range: ₹110–₹145/piece\nMOQ: 50 pieces\nMaterial: Plastic\nShape: Round\nColor: Black\nMounting: Wall mounted\nPackaging: Thermocol box\nUsage: Home, office, decoration',
            'sizes': ['Round'], 'materials': ['Plastic'], 'colors': ['Black'],
            'meta_title': 'Customized Wall Clock Manufacturer Jaipur | HOOVALE',
            'meta_description': 'Customized round wall clock listed at ₹110–₹145/piece with MOQ 50. Share artwork and confirm current quote.',
            'meta_keywords': 'customized wall clock Jaipur, personalized wall clock, photo printed clock',
            'featured': True, 'new': True, 'best': True,
        },
        {
            'name': 'Corporate Clock 12 Inch',
            'slug': 'corporate-clock-12-inch',
            'category': 'corporate-logo-wall-clocks',
            'description': '12-inch promotional corporate wall clock listed under the Hoovale brand. Public listing details include a golden plastic frame, wall mounting, quartz movement, AA battery power and use for corporate gifts, promotion, office and home. Published price range: ₹180–₹230 per piece; MOQ 20 pieces.',
            'short_description': '12-inch golden corporate promotional wall clock.',
            'price': 180, 'moq': 20,
            'specifications': 'Published price range: ₹180–₹230/piece\nMOQ: 20 pieces\nSize: 12 inch\nMaterial: Plastic\nColor: Golden\nType: Promotional wall clock\nMovement: Quartz\nPower: AA battery\nMounting: Wall mounted\nWeight: 450gm',
            'sizes': ['12 inch'], 'materials': ['Plastic'], 'colors': ['Golden'],
            'meta_title': '12 Inch Corporate Wall Clock | HOOVALE Jaipur',
            'meta_description': '12-inch golden corporate promotional wall clock. Published ₹180–₹230/piece, MOQ 20, quartz movement and AA battery.',
            'meta_keywords': '12 inch corporate wall clock, promotional clock Jaipur, corporate gift clock',
            'featured': True, 'new': False, 'best': True,
        },
        {
            'name': 'Antique Wall Clock',
            'slug': 'antique-wall-clock',
            'category': 'home-decorative-wall-clocks',
            'description': 'Blue plastic analog antique-style wall clock listed by Hoovale Ventures for home and decoration. Public listing details include acrylic glass, wall mounting, fine finish and thermocol/paper box packaging. Published price range: ₹90–₹130 per piece; MOQ 50 pieces.',
            'short_description': 'Blue antique-style plastic wall clock.',
            'price': 90, 'moq': 50,
            'specifications': 'Published price range: ₹90–₹130/piece\nMOQ: 50 pieces\nMaterial: Plastic\nColor: Blue\nDisplay: Analog\nGlass: Acrylic\nMounting: Wall mounted\nPackaging: Thermocol / paper box\nFinish: Fine finish',
            'sizes': ['Round'], 'materials': ['Plastic'], 'colors': ['Blue'],
            'meta_title': 'Antique Wall Clock Supplier Jaipur | HOOVALE',
            'meta_description': 'Blue plastic antique-style wall clock with acrylic glass. Published ₹90–₹130/piece and MOQ 50; confirm current quote.',
            'meta_keywords': 'antique wall clock Jaipur, blue wall clock, decorative wall clock supplier',
            'featured': False, 'new': False, 'best': True,
        },
        {
            'name': 'Anchor Wall Clock',
            'slug': 'anchor-wall-clock',
            'category': 'home-decorative-wall-clocks',
            'description': 'Brown anchor-theme analog wall clock listed by Hoovale Ventures for home, office and decoration. Public listing details include wall mounting, thermocol/paper box packaging and fine finish. Published price range: ₹90–₹130 per piece. Confirm current availability and MOQ before ordering.',
            'short_description': 'Brown anchor-theme decorative wall clock.',
            'price': 90, 'moq': 20,
            'specifications': 'Published price range: ₹90–₹130/piece\nMOQ: 20 pieces\nColor: Brown\nDisplay: Analog\nMounting: Wall mounted\nUsage: Home, office, decoration\nPackaging: Thermocol / paper box\nFinish: Fine finish',
            'sizes': ['Round'], 'materials': ['Plastic'], 'colors': ['Brown'],
            'meta_title': 'Anchor Wall Clock Supplier Jaipur | HOOVALE',
            'meta_description': 'Anchor-theme wall clock listed at ₹90–₹130/piece. Public details specify analog display, wall mounting and fine finish.',
            'meta_keywords': 'anchor wall clock Jaipur, decorative anchor clock, wall clock supplier',
            'featured': False, 'new': True, 'best': False,
        },
        {
            'name': 'Plastic Customized Wall Clock',
            'slug': 'plastic-customized-wall-clock',
            'category': 'customized-photo-printed-clocks',
            'description': 'Black plastic customized round wall clock listed for home, office and decoration. Public Hoovale Ventures listings describe wall mounting and thermocol box packaging. Published price range: ₹110–₹145 per piece. Confirm final artwork, quantity and current price before production.',
            'short_description': 'Black plastic customized round wall clock.',
            'price': 110, 'moq': 50,
            'specifications': 'Published price range: ₹110–₹145/piece\nMOQ: 50 pieces\nMaterial: Plastic\nShape: Round\nColor: Black\nMounting: Wall mounted\nPackaging: Thermocol box\nUsage: Home, office, decoration',
            'sizes': ['Round'], 'materials': ['Plastic'], 'colors': ['Black'],
            'meta_title': 'Plastic Customized Wall Clock Jaipur | HOOVALE',
            'meta_description': 'Black plastic customized round wall clock. Published ₹110–₹145/piece with MOQ 50; confirm artwork and current quote.',
            'meta_keywords': 'plastic customized wall clock Jaipur, customized round clock, promotional wall clock',
            'featured': False, 'new': False, 'best': False,
        },
    ]

    product_by_slug = {}
    for data in products:
        data = dict(data)
        category_slug = data.pop('category')
        sizes = data.pop('sizes')
        materials = data.pop('materials', data.pop('materials:', []))
        colors = data.pop('colors')
        data['category'] = cat_by_slug[category_slug]
        data['size_options'] = sizes
        data['material_options'] = materials
        data['color_options'] = colors
        data['image'] = ''
        data['additional_images'] = []
        data['is_active'] = True
        data['brand'] = 'HOOVALE'
        data['availability'] = 'InStock'
        data['sku'] = 'HV-' + data['slug'].upper().replace('-', '')[:30]
        data['og_title'] = data['name'] + ' | HOOVALE'
        data['og_description'] = data['short_description']
        data['is_featured'] = data.pop('featured')
        data['is_new_arrival'] = data.pop('new')
        data['is_bestseller'] = data.pop('best')
        product, _ = Product.objects.update_or_create(
            slug=data['slug'],
            defaults=data
        )
        product_by_slug[data['slug']] = product

    # Responsive campaign banners. They work immediately using static SVG
    # artwork and can later be replaced by real uploaded images from Admin.
    banners = [
        {
            'title': 'Wedding Gifts',
            'slug': 'wedding-gifts',
            'heading': 'Wedding Gifts',
            'subheading': 'Customized wall clocks for weddings, anniversaries and special celebrations.',
            'cta_text': 'Explore Wedding Collection',
            'fallback_desktop': '/static/images/banners/wedding-desktop.svg',
            'fallback_mobile': '/static/images/banners/wedding-mobile.svg',
            'page_heading': 'Wedding & Gifting Wall Clocks',
            'page_subheading': 'Personalized and gifting-focused clock options for memorable occasions.',
            'page_intro': 'Explore wall clock options suitable for wedding, anniversary, festival and gifting requirements. Product availability, customization options and pricing can vary by model and quantity.',
            'page_content': 'For a custom gifting order, share the occasion, quantity, preferred size, artwork or names, and delivery city. HOOVALE can help identify suitable clock options and confirm the current quote before production.',
            'seo_title': 'Wedding Gift Wall Clocks | Customized Gifting | HOOVALE',
            'seo_description': 'Explore wall clocks for wedding and gifting requirements. Discuss customization, quantity and current pricing with HOOVALE Jaipur.',
            'order': 1,
            'products': ['wooden-wall-clocks','customized-wall-clock','plastic-customized-wall-clock'],
        },
        {
            'title': 'Corporate Gifts',
            'slug': 'corporate-gifts',
            'heading': 'Corporate Gifts',
            'subheading': 'Logo-branded clocks for corporate gifting, offices and promotional requirements.',
            'cta_text': 'Explore Corporate Collection',
            'fallback_desktop': '/static/images/banners/corporate-desktop.svg',
            'fallback_mobile': '/static/images/banners/corporate-mobile.svg',
            'page_heading': 'Corporate & Logo Wall Clocks',
            'page_subheading': 'Clock options for business gifting, office use and brand visibility.',
            'page_intro': 'Corporate clock requirements can include logo branding, bulk gifting and office use. Share your quantity and artwork so the suitable model and current price can be confirmed.',
            'page_content': 'For branded orders, the final artwork, print area, clock model, quantity and packaging can affect the quote. Use the enquiry option to discuss your requirement before placing a bulk order.',
            'seo_title': 'Corporate Logo Wall Clocks | Bulk Gifts | HOOVALE Jaipur',
            'seo_description': 'Corporate and logo wall clocks for gifting, office and promotional use. Select products and request a current bulk quote from HOOVALE.',
            'order': 2,
            'products': ['logo-wall-clock','corporate-clock-12-inch','customized-wall-clock'],
        },
        {
            'title': 'Promotional Clocks',
            'slug': 'promotional-clocks',
            'heading': 'Promotional Clocks',
            'subheading': 'Customized clocks for advertising, branding and bulk promotional requirements.',
            'cta_text': 'Explore Promotional Collection',
            'fallback_desktop': '/static/images/banners/promotion-desktop.svg',
            'fallback_mobile': '/static/images/banners/promotion-mobile.svg',
            'page_heading': 'Promotional & Advertising Clocks',
            'page_subheading': 'Practical promotional products that keep your brand visible in everyday spaces.',
            'page_intro': 'Promotional clocks can be used for business gifting, advertising campaigns and other bulk branding requirements. Current models, print options and pricing should be confirmed for each order.',
            'page_content': 'Share the campaign artwork, quantity, preferred clock size and delivery city. HOOVALE can help shortlist a suitable model and confirm the current production and pricing details.',
            'seo_title': 'Promotional Wall Clocks | Advertising Clocks Jaipur | HOOVALE',
            'seo_description': 'Explore promotional and advertising wall clocks for bulk branding. Request current product, customization and pricing details from HOOVALE.',
            'order': 3,
            'products': ['promotional-table-clock','logo-wall-clock','corporate-clock-12-inch'],
        },
        {
            'title': 'Custom Branding',
            'slug': 'custom-branding',
            'heading': 'Custom Branding',
            'subheading': 'Personalized clocks with logo, photo, text or approved campaign artwork.',
            'cta_text': 'Explore Custom Collection',
            'fallback_desktop': '/static/images/banners/custom-desktop.svg',
            'fallback_mobile': '/static/images/banners/custom-mobile.svg',
            'page_heading': 'Custom Branding Wall Clocks',
            'page_subheading': 'Choose a clock and discuss your logo, photo, text or artwork requirements.',
            'page_intro': 'Customized clock orders are suitable for branding, gifting, personal events and promotional use. The final design and print area depend on the selected clock model.',
            'page_content': 'To request customization, share your artwork, preferred clock, quantity and delivery city. Confirm the final proof, price and production details with HOOVALE before the order is processed.',
            'seo_title': 'Custom Branding Wall Clocks | Logo & Photo Printing | HOOVALE',
            'seo_description': 'Customized wall clocks for logo, photo, text and promotional branding. Explore selected products and request a current HOOVALE quote.',
            'order': 4,
            'products': ['logo-wall-clock','customized-wall-clock','plastic-customized-wall-clock'],
        },
        {
            'title': 'Political Campaign Clocks',
            'slug': 'political-campaign-clocks',
            'heading': 'Political Campaign Clocks',
            'subheading': 'Custom clocks for campaign and outreach requirements, subject to approved artwork.',
            'cta_text': 'View Campaign Collection',
            'fallback_desktop': '/static/images/banners/political-desktop.svg',
            'fallback_mobile': '/static/images/banners/political-mobile.svg',
            'page_heading': 'Political Campaign Wall Clocks',
            'page_subheading': 'A dedicated collection for campaign and outreach printing requirements.',
            'page_intro': 'Political campaign clocks can be customized according to approved artwork and quantity requirements. Product availability, print method and pricing should be confirmed for each order.',
            'page_content': 'Share the required artwork, quantity, clock model and delivery city. HOOVALE can provide the current product and customization details for the requested campaign order.',
            'seo_title': 'Political Campaign Wall Clocks | Bulk Custom Clocks | HOOVALE',
            'seo_description': 'Custom wall clocks for political campaign and outreach requirements. Explore the collection and request current pricing from HOOVALE.',
            'order': 5,
            'products': ['political-parties-wall-clock','customized-wall-clock'],
        },
    ]

    for data in banners:
        products_for_banner = data.pop('products')
        defaults = dict(data)
        banner, _ = Banner.objects.update_or_create(
            slug=data['slug'],
            defaults=defaults
        )
        banner.page_products.set([
            product_by_slug[p] for p in products_for_banner if p in product_by_slug
        ])



def ensure_0008_database_schema(apps, schema_editor):
    """
    Reconcile the production database with migration 0008 without dropping data.

    Some Render deployments created part of these columns before Django recorded
    migration 0008. We therefore add only columns/tables that are actually
    missing, while keeping the Django migration state complete.
    """
    connection = schema_editor.connection

    models_and_fields = [
        ('Category', ['static_image_path']),
        ('Banner', [
            'slug', 'desktop_image', 'mobile_image', 'fallback_desktop',
            'fallback_mobile', 'page_heading', 'page_subheading',
            'page_intro', 'page_content', 'page_image', 'seo_title',
            'seo_description', 'seo_keywords', 'is_page_published',
        ]),
    ]

    for model_name, field_names in models_and_fields:
        Model = apps.get_model('products', model_name)
        table = Model._meta.db_table
        with connection.cursor() as cursor:
            existing_columns = {
                col.name
                for col in connection.introspection.get_table_description(
                    cursor, table
                )
            }

        for field_name in field_names:
            field = Model._meta.get_field(field_name)
            if field.column not in existing_columns:
                schema_editor.add_field(Model, field)

    # Ensure the campaign-product M2M table exists as well.
    Banner = apps.get_model('products', 'Banner')
    page_products = Banner._meta.get_field('page_products')
    through_model = page_products.remote_field.through
    through_table = through_model._meta.db_table

    if through_table not in connection.introspection.table_names():
        schema_editor.create_model(through_model)


def ensure_banner_slug_unique(apps, schema_editor):
    """Create a unique index only when the production DB does not already have one."""
    Banner = apps.get_model('products', 'Banner')
    connection = schema_editor.connection
    table = Banner._meta.db_table
    field = Banner._meta.get_field('slug')

    with connection.cursor() as cursor:
        constraints = connection.introspection.get_constraints(cursor, table)

    has_unique_slug = any(
        constraint.get('unique')
        and constraint.get('columns') == [field.column]
        for constraint in constraints.values()
    )

    if not has_unique_slug:
        index_name = 'products_banner_slug_unique_idx'
        quoted_index = schema_editor.quote_name(index_name)
        quoted_table = schema_editor.quote_name(table)
        quoted_column = schema_editor.quote_name(field.column)
        schema_editor.execute(
            f'CREATE UNIQUE INDEX IF NOT EXISTS {quoted_index} '
            f'ON {quoted_table} ({quoted_column})'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_pricingtiertemplate_product_custom_pricing_tiers_and_more'),
    ]

    operations = [
        # Keep migration state complete even when some columns were created by
        # an earlier/manual production deployment.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AddField(
                    model_name='category',
                    name='static_image_path',
                    field=models.CharField(
                        blank=True,
                        default='',
                        help_text='Optional static fallback image path, e.g. /static/images/categories/home-decor.svg',
                        max_length=300,
                    ),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=220, null=True),
                ),
                migrations.AddField(
                    model_name='banner',
                    name='desktop_image',
                    field=models.ImageField(blank=True, null=True, upload_to='banners/desktop/'),
                ),
                migrations.AddField(
                    model_name='banner',
                    name='mobile_image',
                    field=models.ImageField(blank=True, null=True, upload_to='banners/mobile/'),
                ),
                migrations.AddField(
                    model_name='banner',
                    name='fallback_desktop',
                    field=models.CharField(
                        blank=True,
                        default='',
                        help_text='Optional static fallback path, e.g. /static/images/banners/wedding-desktop.svg',
                        max_length=300,
                    ),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='fallback_mobile',
                    field=models.CharField(
                        blank=True,
                        default='',
                        help_text='Optional static fallback path for mobile.',
                        max_length=300,
                    ),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='page_heading',
                    field=models.CharField(blank=True, max_length=220, null=True),
                ),
                migrations.AddField(
                    model_name='banner',
                    name='page_subheading',
                    field=models.CharField(blank=True, default='', max_length=400),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='page_intro',
                    field=models.TextField(blank=True, default=''),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='page_content',
                    field=models.TextField(
                        blank=True,
                        default='',
                        help_text='Main campaign content. Keep it useful and specific to the banner.',
                    ),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='page_image',
                    field=models.ImageField(blank=True, null=True, upload_to='banner_pages/'),
                ),
                migrations.AddField(
                    model_name='banner',
                    name='seo_title',
                    field=models.CharField(blank=True, default='', max_length=70),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='seo_description',
                    field=models.CharField(blank=True, default='', max_length=160),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='seo_keywords',
                    field=models.CharField(blank=True, default='', max_length=400),
                    preserve_default=False,
                ),
                migrations.AddField(
                    model_name='banner',
                    name='is_page_published',
                    field=models.BooleanField(default=True),
                ),
                migrations.AddField(
                    model_name='banner',
                    name='page_products',
                    field=models.ManyToManyField(
                        blank=True,
                        related_name='campaign_banners',
                        to='products.product',
                    ),
                ),
            ],
        ),

        # Reconcile the actual PostgreSQL schema only where something is missing.
        migrations.RunPython(ensure_0008_database_schema, migrations.RunPython.noop),

        # Backfill values after the state/database columns exist.
        migrations.RunPython(backfill_banner_slugs, migrations.RunPython.noop),

        # State-only because these columns may already have the correct
        # production representation. The DB is reconciled above.
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterField(
                    model_name='banner',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=220, unique=True),
                ),
                migrations.AlterField(
                    model_name='banner',
                    name='cta_text',
                    field=models.CharField(blank=True, default='Explore', max_length=100),
                ),
                migrations.AlterField(
                    model_name='banner',
                    name='image',
                    field=models.ImageField(blank=True, null=True, upload_to='banners/'),
                ),
                migrations.AlterField(
                    model_name='banner',
                    name='cta_url',
                    field=models.CharField(blank=True, default='', max_length=500),
                ),
                migrations.AlterField(
                    model_name='banner',
                    name='page_heading',
                    field=models.CharField(blank=True, max_length=220),
                ),
                migrations.AlterModelOptions(
                    name='banner',
                    options={
                        'ordering': ['order', 'created_at'],
                        'verbose_name': 'Homepage / Campaign Banner',
                        'verbose_name_plural': 'Homepage / Campaign Banners',
                    },
                ),
            ],
        ),

        migrations.RunPython(ensure_banner_slug_unique, migrations.RunPython.noop),
        migrations.RunPython(backfill_banner_optional_fields, migrations.RunPython.noop),

        migrations.RunPython(seed_hoovale_catalog, migrations.RunPython.noop),
    ]
