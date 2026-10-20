import { Controller, Get, Param, Render } from '@nestjs/common';
import { CitiesService } from './cities.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class CitiesController {
  constructor(
    private readonly cities: CitiesService,
    private readonly prisma: PrismaService,
  ) {}

  @Get('cities')
  @Render('cities')
  async listPage() {
    const [cities, site] = await Promise.all([
      this.cities.list(),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return {
      cities,
      site,
      pageTitle: 'Wall Clock Supplier Cities | OSIRA',
      metaDescription: 'Find OSIRA wall clock supplier and business-order pages by city, with delivery and enquiry support.',
      canonical: baseUrl ? baseUrl + '/cities' : undefined,
    };
  }

  @Get('cities/:slug')
  @Render('city')
  async detailPage(@Param('slug') slug: string) {
    const [city, site] = await Promise.all([
      this.cities.findBySlug(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const cityUrl = baseUrl ? baseUrl + '/cities/' + city.slug : '/cities/' + city.slug;
    const schemaJsonLd = [{
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      name: city.h1Heading,
      description: city.metaDescription || city.heroSubheading,
      url: cityUrl,
      isPartOf: { '@type': 'WebSite', name: site?.businessName || 'OSIRA', url: baseUrl || undefined }
    },{
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: baseUrl || '/' },
        { '@type': 'ListItem', position: 2, name: 'Cities', item: (baseUrl || '') + '/cities' },
        { '@type': 'ListItem', position: 3, name: city.cityName, item: cityUrl }
      ]
    },{
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: [
        { '@type': 'Question', name: 'Can I enquire about bulk wall clocks in ' + city.cityName + '?', acceptedAnswer: { '@type': 'Answer', text: 'Yes. Share your quantity, preferred designs, use case and delivery city. Current availability and commercial terms can then be confirmed for the requirement.' } },
        { '@type': 'Question', name: 'Can wall clocks be used for corporate gifting or branding?', acceptedAnswer: { '@type': 'Answer', text: 'OSIRA accepts enquiries for corporate gifting, promotional and custom-branded requirements. Logo options, artwork, minimum quantities and production timelines must be confirmed for each order.' } },
        { '@type': 'Question', name: 'How do I confirm price and delivery time?', acceptedAnswer: { '@type': 'Answer', text: 'Send the product or collection, quantity and delivery PIN code. Pricing and dispatch estimates depend on the selected product and order details.' } }
      ]
    }];
    return {
      city,
      site,
      schemaJsonLd,
      pageTitle: city.slug === 'jaipur' ? 'Wall Clock Manufacturer in Jaipur | OSIRA' : (city.metaTitle || city.h1Heading + ' | OSIRA'),
      metaDescription: city.slug === 'jaipur' ? 'Explore wall clocks for retail, offices, corporate gifting and custom branding from OSIRA, the Jaipur-based wall clock brand of Omaansh Industries.' : (city.metaDescription || city.heroSubheading || city.introContent.slice(0, 155)),
      canonical: baseUrl ? baseUrl + '/cities/' + city.slug : undefined,
    };
  }

  @Get('api/cities')
  async apiList() { return this.cities.list(); }

  @Get('api/cities/:slug')
  async apiDetail(@Param('slug') slug: string) { return this.cities.findBySlug(slug); }
}
