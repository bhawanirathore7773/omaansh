import { Controller, Get, Param, Render } from '@nestjs/common';
import { ServicesService } from './services.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class ServicesController {
  constructor(
    private readonly services: ServicesService,
    private readonly prisma: PrismaService,
  ) {}

  @Get('services')
  @Render('services')
  async servicesPage() {
    const [services, site] = await Promise.all([
      this.services.list(),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return {
      services,
      site,
      pageTitle: 'Wall Clock Manufacturing & Business Services | OSIRA',
      metaDescription: 'Explore OSIRA wall clock manufacturing, wholesale, corporate gifting, promotional branding and custom OEM services.',
      canonical: baseUrl ? baseUrl + '/services' : undefined,
    };
  }

  @Get('services/:slug')
  @Render('service')
  async servicePage(@Param('slug') slug: string) {
    const [service, site] = await Promise.all([
      this.services.findBySlug(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const selectedProductIds = Array.isArray(service.productIds) ? service.productIds.map(Number).filter(id => Number.isInteger(id) && id > 0) : [];
    const serviceProducts = selectedProductIds.length ? await this.prisma.product.findMany({ where: { id: { in: selectedProductIds }, isActive: true }, include: { category: true } }) : [];
    const productOrder = new Map(selectedProductIds.map((id, index) => [id, index]));
    serviceProducts.sort((a, b) => (productOrder.get(a.id) ?? 999) - (productOrder.get(b.id) ?? 999));
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return {
      service,
      serviceProducts,
      site,
      pageTitle: service.metaTitle || service.h1Heading + ' | OSIRA',
      metaDescription: service.metaDescription || service.shortDescription,
      canonical: baseUrl ? baseUrl + '/services/' + service.slug : undefined,
    };
  }

  @Get('api/services')
  async servicesApi() {
    return this.services.list();
  }

  @Get('api/services/:slug')
  async serviceApi(@Param('slug') slug: string) {
    return this.services.findBySlug(slug);
  }
}
