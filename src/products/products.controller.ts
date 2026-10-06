import { Controller, Get, Param, Query, Render } from '@nestjs/common';
import { ProductsService } from './products.service';

@Controller()
export class ProductsController {
  constructor(private readonly products: ProductsService) {}

  @Get('products')
  @Render('products')
  async productsPage(@Query('q') q?: string) {
    return { products: await this.products.list(q) };
  }

  @Get('products/:slug')
  @Render('product')
  async productPage(@Param('slug') slug: string) {
    const [product, related] = await Promise.all([
      this.products.findBySlug(slug),
      this.products.related(slug),
    ]);
    return { product, related };
  }

  @Get('api/products')
  async productsApi(@Query('q') q?: string) {
    return this.products.list(q);
  }

  @Get('api/products/:slug')
  async productApi(@Param('slug') slug: string) {
    return this.products.findBySlug(slug);
  }
}
