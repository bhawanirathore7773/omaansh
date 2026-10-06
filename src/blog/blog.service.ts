import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class BlogService {
  constructor(private readonly prisma: PrismaService) {}

  async list() {
    return this.prisma.blog.findMany({
      where: { isPublished: true },
      orderBy: { createdAt: 'desc' },
    });
  }

  async findBySlug(slug: string) {
    const post = await this.prisma.blog.findUnique({ where: { slug } });
    if (!post || !post.isPublished) throw new NotFoundException('Article not found');
    return post;
  }
}
