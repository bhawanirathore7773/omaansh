import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ServicesService {
  constructor(private readonly prisma: PrismaService) {}

  async list() {
    return this.prisma.servicePage.findMany({
      where: { isPublished: true },
      orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }],
    });
  }

  async findBySlug(slug: string) {
    const service = await this.prisma.servicePage.findUnique({ where: { slug } });
    if (!service || !service.isPublished) {
      throw new NotFoundException('Service not found');
    }
    return service;
  }
}
