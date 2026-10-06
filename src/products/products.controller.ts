import { Controller, Get, Param, Query, Render } from '@nestjs/common';
import { ProductsService } from './products.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class ProductsController {
  constructor(
    private readonly products: ProductsService,
    private readonly prisma: PrismaService,
  ) {}

  @Get('products')
  @Render('products')
  async productsPage(
    @Query('q') q?: string,
    @Query('category') category?: string,
  ) {
    const [products, categories, site] = await Promise.all([
      this.products.list(q, category),
      this.prisma.category.findMany({
        orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }],
      }),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);

    return {
      products,
      categories,
      site,
      q: q || '',
      category: category || '',
    };
  }

  @Get('products/:slug')
  @Render('product')
  async productPage(@Param('slug') slug: string) {
    const [product, related, site] = await Promise.all([
      this.products.findBySlug(slug),
      this.products.related(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);

    return { product, related, site };
  }

  @Get('api/products')
  async productsApi(
    @Query('q') q?: string,
    @Query('category') category?: string,
  ) {
    return this.products.list(q, category);
  }

  @Get('api/products/:slug')
  async productApi(@Param('slug') slug: string) {
    return this.products.findBySlug(slug);
  }
}
