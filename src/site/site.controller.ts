import { Controller, Get, Render } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class SiteController {
  constructor(private readonly prisma: PrismaService) {}

  @Get()
  @Render('home')
  async home() {
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

    return { site, categories, featuredProducts };
  }

  @Get('health')
  health() {
    return { ok: true, service: 'osira-web', timestamp: new Date().toISOString() };
  }
}
