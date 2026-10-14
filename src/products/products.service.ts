import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ProductsService {
  constructor(private readonly prisma: PrismaService) {}

  async list(query?: string, categorySlug?: string, size?: string, application?: string, page = 1, limit = 24, minPrice?: string, maxPrice?: string, sort = 'recommended') {
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
    const filters: any[] = [];
    if (size?.trim()) filters.push({ specifications: { contains: size.trim() } });
    if (application?.trim()) filters.push({ specifications: { contains: application.trim() } });
    const priceFilter: any = {};
    if (minPrice && Number.isFinite(Number(minPrice)) && Number(minPrice) >= 0) priceFilter.gte = Number(minPrice);
    if (maxPrice && Number.isFinite(Number(maxPrice)) && Number(maxPrice) >= 0) priceFilter.lte = Number(maxPrice);
    if (Object.keys(priceFilter).length) where.price = priceFilter;
    if (filters.length) where.AND = filters;
    const orderBy: any = sort === 'price-low' ? [{ price: 'asc' }, { createdAt: 'desc' }] : sort === 'price-high' ? [{ price: 'desc' }, { createdAt: 'desc' }] : sort === 'newest' ? [{ createdAt: 'desc' }] : sort === 'name' ? [{ name: 'asc' }] : [{ isFeatured: 'desc' }, { isNewArrival: 'desc' }, { createdAt: 'desc' }];

    const [items, total] = await Promise.all([
      this.prisma.product.findMany({
        where,
        include: { category: true },
        orderBy,
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
