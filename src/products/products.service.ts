import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ProductsService {
  constructor(private readonly prisma: PrismaService) {}

  async list(query?: string, categorySlug?: string) {
    return this.prisma.product.findMany({
      where: {
        isActive: true,
        ...(query
          ? {
              OR: [
                { name: { contains: query } },
                { shortDescription: { contains: query } },
              ],
            }
          : {}),
        ...(categorySlug ? { category: { slug: categorySlug } } : {}),
      },
      include: { category: true },
      orderBy: [{ isFeatured: 'desc' }, { createdAt: 'desc' }],
    });
  }

  async findBySlug(slug: string) {
    const product = await this.prisma.product.findUnique({
      where: { slug },
      include: { category: true, pricingTierTemplate: true },
    });

    if (!product || !product.isActive) {
      throw new NotFoundException('Product not found');
    }

    return product;
  }

  async related(slug: string) {
    const current = await this.prisma.product.findUnique({
      where: { slug },
      select: { id: true, categoryId: true },
    });

    if (!current) return [];

    return this.prisma.product.findMany({
      where: {
        isActive: true,
        id: { not: current.id },
        categoryId: current.categoryId,
      },
      include: { category: true },
      orderBy: { createdAt: 'desc' },
      take: 6,
    });
  }
}
