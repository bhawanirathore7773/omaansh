import { Controller, Get, Param, Render } from '@nestjs/common';
import { CategoriesService } from './categories.service';

@Controller()
export class CategoriesController {
  constructor(private readonly categories: CategoriesService) {}

  @Get('categories')
  @Render('categories')
  async categoriesPage() {
    return { categories: await this.categories.list() };
  }

  @Get('categories/:slug')
  @Render('category')
  async categoryPage(@Param('slug') slug: string) {
    return { category: await this.categories.findBySlug(slug) };
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
