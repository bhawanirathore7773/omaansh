import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ProductsService {
  constructor(private readonly prisma: PrismaService) {}

  async list(query?: string, categorySlug?: string, size?: string, application?: string, page = 1, limit = 24) {
    const safePage = Math.max(1, Number(page) || 1);
    const safeLimit = Math.min(48, Math.max(12, Number(limit) || 24));
    const where: any = { isActive: true };
    if (query?.trim()) {
      const q = query.trim();
      where.OR = [
        { name: { contains: q } },
        { shortDescription: { contains: q } },
        { description: { contains: q } },
        { specifications: { contains: q } },
      ];
    }
    if (categorySlug) where.category = { slug: categorySlug };
    if (size?.trim()) where.specifications = { contains: 'Size: ' + size.trim() };
    if (application?.trim()) where.specifications = { contains: application.trim() };

    const [items, total] = await Promise.all([
      this.prisma.product.findMany({
        where,
        include: { category: true },
        orderBy: [{ isFeatured: 'desc' }, { isNewArrival: 'desc' }, { createdAt: 'desc' }],
        skip: (safePage - 1) * safeLimit,
        take: safeLimit,
      }),
      this.prisma.product.count({ where }),
    ]);

    return { items, total, page: safePage, limit: safeLimit, totalPages: Math.max(1, Math.ceil(total / safeLimit)) };
  }

  async findBySlug(slug: string) {
    const product = await this.prisma.product.findUnique({
      where: { slug },
      include: { category: true, pricingTierTemplate: true },
    });
    if (!product || !product.isActive) throw new NotFoundException('Product not found');
    return product;
  }

  async related(slug: string) {
    const current = await this.prisma.product.findUnique({ where: { slug }, select: { id: true, categoryId: true } });
    if (!current) return [];
    return this.prisma.product.findMany({
      where: { isActive: true, id: { not: current.id }, categoryId: current.categoryId },
      include: { category: true },
      orderBy: [{ isFeatured: 'desc' }, { createdAt: 'desc' }],
      take: 6,
    });
  }
}
