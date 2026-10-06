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
    return {
      city,
      site,
      pageTitle: city.metaTitle || city.h1Heading + ' | OSIRA',
      metaDescription: city.metaDescription || city.heroSubheading || city.introContent.slice(0, 155),
      canonical: baseUrl ? baseUrl + '/cities/' + city.slug : undefined,
    };
  }

  @Get('api/cities')
  async apiList() { return this.cities.list(); }

  @Get('api/cities/:slug')
  async apiDetail(@Param('slug') slug: string) { return this.cities.findBySlug(slug); }
}
