import { Controller, Get, Param, Query, Render } from '@nestjs/common';
import { ProductsService } from './products.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class ProductsController {
  constructor(private readonly products: ProductsService, private readonly prisma: PrismaService) {}

  @Get('products')
  @Render('products')
  async productsPage(@Query('q') q?: string, @Query('category') category?: string) {
    const [products, categories, site] = await Promise.all([
      this.products.list(q, category),
      this.prisma.category.findMany({ orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }] }),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);

    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const canonicalPath = category ? '/products?category=' + encodeURIComponent(category) : '/products';

    return {
      products, categories, site, q: q || '', category: category || '',
      pageTitle: category ? category.replace(/-/g, ' ') + ' Wall Clocks | OSIRA' : 'Wall Clocks | Wholesale, Custom & Business Orders | OSIRA',
      metaDescription: 'Browse OSIRA wall clocks for retail, wholesale, corporate gifting, promotional branding and custom business orders.',
      canonical: baseUrl ? baseUrl + canonicalPath : undefined,
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
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const productUrl = baseUrl ? baseUrl + '/products/' + product.slug : '/products/' + product.slug;
    const schemaJsonLd = [
      {
        '@context': 'https://schema.org',
        '@type': 'Product',
        name: product.name,
        description: product.shortDescription || product.description,
        image: product.image ? [product.image] : undefined,
        sku: product.sku || undefined,
        brand: { '@type': 'Brand', name: product.brand || 'OSIRA' },
        category: product.category?.name,
        offers: product.price ? {
          '@type': 'Offer',
          url: productUrl,
          priceCurrency: 'INR',
          price: Number(product.price),
          availability: 'https://schema.org/' + (product.availability === 'InStock' ? 'InStock' : 'PreOrder')
        } : undefined
      },
      {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: baseUrl || '/' },
          { '@type': 'ListItem', position: 2, name: 'Wall Clocks', item: (baseUrl || '') + '/products' },
          ...(product.category ? [{ '@type': 'ListItem', position: 3, name: product.category.name, item: (baseUrl || '') + '/categories/' + product.category.slug }] : []),
          { '@type': 'ListItem', position: product.category ? 4 : 3, name: product.name, item: productUrl }
        ]
      }
    ];

    return {
      product, related, site, schemaJsonLd,
      pageTitle: product.metaTitle || product.name + ' | OSIRA Wall Clocks',
      metaDescription: product.metaDescription || product.shortDescription || 'Explore ' + product.name + ' from OSIRA for retail, wholesale and business orders.',
      canonical: baseUrl ? baseUrl + '/products/' + product.slug : undefined,
    };
  }

  @Get('api/products')
  async productsApi(@Query('q') q?: string, @Query('category') category?: string) {
    return this.products.list(q, category);
  }

  @Get('api/products/:slug')
  async productApi(@Param('slug') slug: string) {
    return this.products.findBySlug(slug);
  }
}
