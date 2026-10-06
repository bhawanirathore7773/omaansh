import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class CitiesService {
  constructor(private readonly prisma: PrismaService) {}

  async list() {
    return this.prisma.cityPage.findMany({
      where: { isPublished: true },
      orderBy: [{ displayOrder: 'asc' }, { cityName: 'asc' }],
    });
  }

  async findBySlug(slug: string) {
    const city = await this.prisma.cityPage.findUnique({ where: { slug } });
    if (!city || !city.isPublished) throw new NotFoundException('City page not found');
    return city;
  }
}
