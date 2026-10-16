import { Controller, Get, Header, Query, Render, Param, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class SiteController {
  constructor(private readonly prisma: PrismaService) {}

  @Get()
  @Render('home')
  async home(@Query('enquiry') enquiry?: string) {

    const bannerCount = await this.prisma.homeBanner.count();
    if (bannerCount === 0) {
      await this.prisma.homeBanner.createMany({ data: [
        { title: 'Wall clocks for every space', subtitle: 'Explore practical and decorative designs for homes, offices and retail.', buttonLabel: 'Explore collections', linkUrl: '/categories', backgroundColor: '#17212b', displayOrder: 1, isActive: true },
        { title: 'Wholesale wall clock supply', subtitle: 'Planning a retail or distribution order? Share your product and quantity requirements.', buttonLabel: 'Wholesale enquiries', linkUrl: '/services/wholesale-wall-clocks', backgroundColor: '#263d50', displayOrder: 2, isActive: true },
        { title: 'Make your brand part of the moment', subtitle: 'Discuss promotional wall clocks, logo artwork and corporate gifting requirements.', buttonLabel: 'Discuss custom orders', linkUrl: '/services/promotional-wall-clocks', backgroundColor: '#573b32', displayOrder: 3, isActive: true },
        { title: 'Need a tailored business order?', subtitle: 'Tell us the preferred style, quantity, branding and delivery city for a quotation.', buttonLabel: 'Request a quotation', linkUrl: '/#enquiry', backgroundColor: '#303c35', displayOrder: 4, isActive: true },
      ] });
    }
    const [site, categories, featuredProducts, banners] = await Promise.all([
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
      this.prisma.category.findMany({ orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }], take: 8 }),
      this.prisma.product.findMany({
        where: { isActive: true, isFeatured: true },
        include: { category: true },
        orderBy: { createdAt: 'desc' },
        take: 6,
      }),
      this.prisma.homeBanner.findMany({ where: { isActive: true }, orderBy: { displayOrder: 'asc' } }),
    ]);

    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const siteUrl = baseUrl || undefined;
    const organization = {
      '@context': 'https://schema.org',
      '@type': 'Organization',
      name: site?.businessName || 'OSIRA',
      url: siteUrl,
      logo: siteUrl ? siteUrl + '/favicon.svg' : undefined,
      telephone: site?.primaryPhone || undefined,
      email: site?.email || undefined,
      address: site ? {
        '@type': 'PostalAddress',
        streetAddress: site.streetAddress,
        addressLocality: site.locality,
        addressRegion: site.region,
        postalCode: site.postalCode,
        addressCountry: site.country || 'IN'
      } : undefined,
      geo: site?.latitude && site?.longitude ? {
        '@type': 'GeoCoordinates',
        latitude: site.latitude,
        longitude: site.longitude
      } : undefined,
      sameAs: [site?.facebookUrl, site?.instagramUrl, site?.youtubeUrl, site?.linkedinUrl, site?.indiamartUrl].filter(Boolean)
    };
    const website = {
      '@context': 'https://schema.org',
      '@type': 'WebSite',
      name: site?.businessName || 'OSIRA',
      url: siteUrl,
      potentialAction: {
        '@type': 'SearchAction',
        target: siteUrl ? siteUrl + '/products?q={search_term_string}' : '/products?q={search_term_string}',
        'query-input': 'required name=search_term_string'
      }
    };
    return {
      site,
      categories,
      banners,
      schemaJsonLd: [organization, website],
      featuredProducts,
      enquirySent: enquiry === 'sent',
      pageTitle: site?.defaultMetaTitle || 'OSIRA | Wall Clock Manufacturer & Supplier in Jaipur',
      metaDescription: site?.defaultMetaDescription || 'OSIRA creates wall clocks and décor products for homes, workplaces and commercial spaces, with custom and business order support.',
      canonical: process.env.SITE_URL || undefined,
    };
  }

  @Get('reseller')
  @Render('reseller')
  async reseller() {
    let settings = await this.prisma.resellerPageSettings.findUnique({ where: { id: 1 } });
    if (!settings) {
      settings = await this.prisma.resellerPageSettings.create({ data: { id: 1 } });
    }
    if (!settings.isPublished) throw new NotFoundException('Reseller programme is not published.');
    const demo: any[] = [
        { name:'ABS Plastic Clock Body', slug:'abs-plastic-clock-body', componentType:'Body & back cover', shortDescription:'Lightweight moulded body options for everyday retail and bulk clock programmes.', description:'Plastic bodies and rear covers are selected around the clock design, target price, dial size and assembly fit. Ask us to confirm the exact polymer/grade, wall thickness, mounting design, finish and compatibility for the model you need.', image:'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1000&q=82', gallery:['https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=82'], sizes:['8 inch','10 inch','12 inch'], colors:['Black','White','Ivory','Custom colours subject to MOQ'], styles:['Plain body','Decorative bezel','Custom brand programme'], movementTypes:[], specifications:[{key:'Common use',value:'Everyday and promotional wall clocks'},{key:'Material confirmation',value:'Confirm polymer/grade per selected model'},{key:'Fitment',value:'Match body, dial, glass and movement together'},{key:'Customisation',value:'Colour and branding availability on request'}], qualityPoints:['Check mould finish and visible surface consistency','Confirm mounting slot and movement clearance','Request a sample/reference before a large order'], orderingNotes:'Demo guide only. Exact material grade, colours, MOQ and price must be confirmed for the selected model.', displayOrder:1, isPublished:true },
        { name:'Clock Dial Glass', slug:'clock-dial-glass', componentType:'Front glass / lens', shortDescription:'Clear front lens options that protect the dial and help the clock look finished.', description:'The front lens protects the dial from dust and handling while influencing clarity, reflection and the overall finish. The right option depends on diameter, bezel design, intended environment and the selected clock construction.', image:'https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1000&q=82', gallery:['https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=82'], sizes:['8 inch','10 inch','12 inch'], colors:['Clear','Tinted options only if available for the model'], styles:['Flat lens','Model-specific shaped lens'], movementTypes:[], specifications:[{key:'Purpose',value:'Dial protection and visual clarity'},{key:'Fit',value:'Diameter and bezel-specific'},{key:'Finish',value:'Confirm clarity, reflection and edge fit'},{key:'Handling',value:'Check for scratches and edge damage'}], qualityPoints:['Inspect clarity under normal room lighting','Check diameter, edge finish and seating','Confirm the lens is compatible with the chosen ring/body'], orderingNotes:'Image is illustrative, not a guaranteed sample of supplied glass. Confirm material and specification before purchase.', displayOrder:2, isPublished:true },
        { name:'Bezel / Outer Ring', slug:'bezel-outer-ring', componentType:'Bezel & outer ring', shortDescription:'The visible outer frame that defines the clock style and finish.', description:'The bezel or outer ring creates the clock’s visible profile. Finish, profile and compatibility vary across designs; a metallic-looking finish does not by itself establish that a part is solid metal. Ask for the exact construction and finish for the selected reference.', image:'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=1000&q=82', gallery:['https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=900&q=82'], sizes:['8 inch','10 inch','12 inch'], colors:['Black','Silver','Gold-tone','White'], styles:['Minimal round','Decorative profile','Contemporary finish'], movementTypes:[], specifications:[{key:'Role',value:'Visual frame and component fit'},{key:'Finish options',value:'Model-dependent colour and coating'},{key:'Compatibility',value:'Must match body and front lens'},{key:'Care',value:'Avoid abrasive cleaners on coated finishes'}], qualityPoints:['Check finish uniformity and joints','Inspect for scratches, dents and coating defects','Confirm exact diameter and mounting method'], orderingNotes:'Colour names are indicative. Actual shade and finish depend on the available production model.', displayOrder:3, isPublished:true },
        { name:'Quartz Clock Movement', slug:'quartz-clock-movement', componentType:'Movement / mechanism', shortDescription:'The mechanism that drives the hands; confirm shaft length and movement type.', description:'Clock movements are not interchangeable by appearance alone. Shaft length, hand fitting, dial thickness, power source, hand load and ticking/sweep behaviour should be confirmed against the actual clock assembly before ordering.', image:'https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=1000&q=82', gallery:['https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=900&q=82'], sizes:['For 8 inch models','For 10 inch models','For 12 inch models'], colors:['Black housing is common; confirm current option'], styles:['Standard quartz','Sweep / silent style only when specified'], movementTypes:['Standard quartz','Sweep / silent mechanism (availability to confirm)'], specifications:[{key:'Power',value:'Typically battery operated; confirm exact model'},{key:'Shaft length',value:'Must suit dial thickness and hand stack'},{key:'Hand fitting',value:'Confirm shaft/thread and hand-hole compatibility'},{key:'Sound profile',value:'Standard tick or sweep depends on mechanism'}], qualityPoints:['Confirm the exact movement reference and shaft length','Check hand compatibility and clearance','Ask about sound profile and warranty terms'], orderingNotes:'Do not assume silent/sweep or shaft dimensions without written confirmation for the chosen model.', displayOrder:4, isPublished:true },
        { name:'Clock Hands & Dial Markers', slug:'clock-hands-dial-markers', componentType:'Hands & dial details', shortDescription:'Hands and markers affect readability, contrast and the finished design.', description:'Hands and dial markers should be selected together for visual contrast, fit and clearance. Length, hole fitting, finish and dial layout depend on the clock diameter and design.', image:'https://images.unsplash.com/photo-1490312278390-ab64016e0aa9?auto=format&fit=crop&w=1000&q=82', gallery:['https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=900&q=82'], sizes:['8 inch','10 inch','12 inch'], colors:['Black','White','Gold-tone','Silver-tone'], styles:['Numeral dial','Index markers','Minimal hands','Decorative hands'], movementTypes:[], specifications:[{key:'Compatibility',value:'Movement shaft and hand-hole must match'},{key:'Length',value:'Select for dial radius and clock size'},{key:'Clearance',value:'Hands must not rub each other, glass or dial'},{key:'Readability',value:'Use adequate contrast against dial colour'}], qualityPoints:['Check hand alignment and balance','Confirm minute/hour hand lengths','Review dial contrast and clearances before assembly'], orderingNotes:'Actual shapes, finishes and dimensions vary by model; request a matching set rather than mixing unverified parts.', displayOrder:5, isPublished:true },
        { name:'Dial / Face Plate', slug:'clock-dial-face-plate', componentType:'Dial & face plate', shortDescription:'The visible face that sets the clock’s layout, typography and overall identity.', description:'Dial options define the reading experience and product character. Before confirming a dial, review print quality, colour consistency, number/index layout, hand contrast and fit with the bezel and movement shaft.', image:'https://images.unsplash.com/photo-1507643179773-3e975d7ac515?auto=format&fit=crop&w=1000&q=82', gallery:['https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=82'], sizes:['8 inch','10 inch','12 inch'], colors:['White','Black','Ivory','Design-specific colours'], styles:['Arabic numerals','Index markers','Minimal','Custom printed artwork subject to approval'], movementTypes:[], specifications:[{key:'Layout',value:'Numerals, indices and artwork vary by design'},{key:'Print quality',value:'Check alignment, legibility and finish'},{key:'Fit',value:'Confirm diameter, centre hole and hand clearance'},{key:'Branding',value:'Artwork and MOQ require review'}], qualityPoints:['Review artwork proof before production','Check print alignment and colour consistency','Match dial with hands, glass and case'], orderingNotes:'Custom printing and logo work are subject to artwork approval, feasibility and minimum order quantity.', displayOrder:6, isPublished:true },
    ];
    if ((await this.prisma.resellerMaterial.count()) < demo.length) {
      for (const item of demo) {
        const exists = await this.prisma.resellerMaterial.findUnique({ where: { slug: item.slug }, select: { id: true } });
        if (!exists) await this.prisma.resellerMaterial.create({ data: item as any });
      }
    }
    const [site, materials] = await Promise.all([
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
      this.prisma.resellerMaterial.findMany({ where: { isPublished: true }, orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }] }),
    ]);
    const base = (process.env.SITE_URL || 'https://omaansh.com').replace(/\/$/, '');
    return {
      site, settings, materials,
      pageTitle: 'Wall Clock Components & Wholesale Reseller Programme | OSIRA',
      metaDescription: 'Explore wall clock components, clock body, glass, bezel, dial, hands and quartz movement options in 8, 10 and 12 inch sizes. Ask OSIRA about wholesale availability and specifications.',
      canonical: base + '/reseller',
    };
  }

  @Get('reseller/materials/:slug')
  @Render('reseller-material')
  async resellerMaterial(@Param('slug') slug: string) {
    const [site, settings, material] = await Promise.all([
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
      this.prisma.resellerPageSettings.findUnique({ where: { id: 1 } }),
      this.prisma.resellerMaterial.findFirst({ where: { slug, isPublished: true } }),
    ]);
    if (settings && !settings.isPublished) throw new NotFoundException('Reseller programme is not published.');
    if (!material) {
      return { site, settings: settings || { whatsappIntro: 'Hello OSIRA, please share reseller component details.' }, material: null, pageTitle: 'Component not found | OSIRA', metaDescription: 'This component is not currently available.', canonical: undefined };
    }
    return {
      site, settings: settings || { whatsappIntro: 'Hello OSIRA, please share reseller component details.' }, material,
      pageTitle: material.name + ' | Wall Clock Component Guide | OSIRA',
      metaDescription: material.shortDescription,
      canonical: (process.env.SITE_URL || 'https://omaansh.com').replace(/\/$/, '') + '/reseller/materials/' + material.slug,
    };
  }

  @Get('about')
  @Render('about')
  async about() {
    const site = await this.prisma.siteSettings.findUnique({ where: { id: 1 } });
    return {
      site,
      pageTitle: 'About OSIRA | Wall Clock Supplier for Business Orders',
      metaDescription: 'Learn about OSIRA wall clocks for retail, wholesale, corporate gifting and custom business requirements.',
      canonical: process.env.SITE_URL ? process.env.SITE_URL.replace(/\/$/, '') + '/about' : undefined,
    };
  }

  @Get('robots.txt')
  @Header('Content-Type', 'text/plain; charset=utf-8')
  robots() {
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return ['User-agent: *', 'Allow: /', 'Disallow: /admin', 'Disallow: /api', 'Sitemap: ' + (baseUrl ? baseUrl + '/sitemap.xml' : '/sitemap.xml')].join('\n');
  }

  @Get('sitemap.xml')
  @Header('Content-Type', 'application/xml; charset=utf-8')
  async sitemap() {
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const [products, categories, services, industries, cities, blogs, resellerMaterials] = await Promise.all([
      this.prisma.product.findMany({ where: { isActive: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.category.findMany({ select: { slug: true, updatedAt: true } }),
      this.prisma.servicePage.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.industryPage.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.cityPage.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.blog.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.resellerMaterial.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
    ]);
    const urls: Array<[string, Date]> = [
      ['', new Date()], ['/products', new Date()], ['/categories', new Date()], ['/about', new Date()],
      ...products.map(x => ['/products/' + x.slug, x.updatedAt] as [string, Date]),
      ...categories.map(x => ['/categories/' + x.slug, x.updatedAt] as [string, Date]),
      ...services.map(x => ['/services/' + x.slug, x.updatedAt] as [string, Date]),
      ...industries.map(x => ['/industries/' + x.slug, x.updatedAt] as [string, Date]),
      ...cities.map(x => ['/cities/' + x.slug, x.updatedAt] as [string, Date]),
      ...blogs.map(x => ['/blog/' + x.slug, x.updatedAt] as [string, Date]),
      ['/reseller', new Date()],
      ...resellerMaterials.map(x => ['/reseller/materials/' + x.slug, x.updatedAt] as [string, Date]),
    ];
    const xml = urls.map(([path, updatedAt]) => {
      const loc = (baseUrl ? baseUrl : '') + (path || '/');
      return '<url><loc>' + loc.replace(/&/g, '&amp;') + '</loc><lastmod>' + new Date(updatedAt).toISOString() + '</lastmod></url>';
    }).join('');
    return '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + xml + '</urlset>';
  }
  @Get('health')
  @Header('Cache-Control', 'no-store')
  health() {
    return { ok: true, service: 'osira-web', timestamp: new Date().toISOString() };
  }
}
