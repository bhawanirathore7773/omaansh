import { Controller, Get, Param, Render } from '@nestjs/common';
import { CategoriesService } from './categories.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class CategoriesController {
  constructor(
    private readonly categories: CategoriesService,
    private readonly prisma: PrismaService,
  ) {}

  @Get('categories')
  @Render('categories')
  async categoriesPage() {
    const [categories, site] = await Promise.all([
      this.categories.list(),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    return { categories, site };
  }

  @Get('categories/:slug')
  @Render('category')
  async categoryPage(@Param('slug') slug: string) {
    const [category, site] = await Promise.all([
      this.categories.findBySlug(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    return { category, site };
  }

  @Get('api/categories')
  async categoriesApi() {
    return this.categories.list();
  }

  @Get('api/categories/:slug')
  async categoryApi(@Param('slug') slug: string) {
    return this.categories.findBySlug(slug);
  }
}
