import { Controller, Get, Header, Query, Render } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class SiteController {
  constructor(private readonly prisma: PrismaService) {}

  @Get()
  @Render('home')
  async home(@Query('enquiry') enquiry?: string) {
    const [site, categories, featuredProducts] = await Promise.all([
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
      this.prisma.category.findMany({ orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }], take: 8 }),
      this.prisma.product.findMany({
        where: { isActive: true, isFeatured: true },
        include: { category: true },
        orderBy: { createdAt: 'desc' },
        take: 6,
      }),
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
      schemaJsonLd: [organization, website],
      featuredProducts,
      enquirySent: enquiry === 'sent',
      pageTitle: site?.defaultMetaTitle || 'OSIRA | Wall Clock Manufacturer & Supplier in Jaipur',
      metaDescription: site?.defaultMetaDescription || 'OSIRA creates wall clocks and décor products for homes, workplaces and commercial spaces, with custom and business order support.',
      canonical: process.env.SITE_URL || undefined,
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
    const [products, categories, services, industries, cities, blogs] = await Promise.all([
      this.prisma.product.findMany({ where: { isActive: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.category.findMany({ select: { slug: true, updatedAt: true } }),
      this.prisma.servicePage.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.industryPage.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.cityPage.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
      this.prisma.blog.findMany({ where: { isPublished: true }, select: { slug: true, updatedAt: true } }),
    ]);
    const urls: Array<[string, Date]> = [
      ['', new Date()], ['/products', new Date()], ['/categories', new Date()],
      ...products.map(x => ['/products/' + x.slug, x.updatedAt] as [string, Date]),
      ...categories.map(x => ['/categories/' + x.slug, x.updatedAt] as [string, Date]),
      ...services.map(x => ['/services/' + x.slug, x.updatedAt] as [string, Date]),
      ...industries.map(x => ['/industries/' + x.slug, x.updatedAt] as [string, Date]),
      ...cities.map(x => ['/cities/' + x.slug, x.updatedAt] as [string, Date]),
      ...blogs.map(x => ['/blog/' + x.slug, x.updatedAt] as [string, Date]),
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
