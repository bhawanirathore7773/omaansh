import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class IndustriesService {
  constructor(private readonly prisma: PrismaService) {}

  async list() {
    return this.prisma.industryPage.findMany({
      where: { isPublished: true },
      include: { featuredProducts: { include: { product: true } } },
      orderBy: [{ displayOrder: 'asc' }, { industryName: 'asc' }],
    });
  }

  async findBySlug(slug: string) {
    const industry = await this.prisma.industryPage.findUnique({
      where: { slug },
      include: {
        featuredProducts: {
          include: { product: { include: { category: true } } },
        },
      },
    });
    if (!industry || !industry.isPublished) throw new NotFoundException('Industry page not found');
    return industry;
  }
}
