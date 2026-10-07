import { Controller, Get, Param, Query, Render } from '@nestjs/common';
import { ProductsService } from './products.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class ProductsController {
  constructor(private readonly products: ProductsService, private readonly prisma: PrismaService) {}

  @Get('products')
  @Render('products')
  async productsPage(
    @Query('q') q?: string,
    @Query('category') category?: string,
    @Query('size') size?: string,
    @Query('application') application?: string,
    @Query('page') page = '1',
  ) {
    const [result, categories, site] = await Promise.all([
      this.products.list(q, category, size, application, Number(page)),
      this.prisma.category.findMany({ orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }] }),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const params = new URLSearchParams();
    if (q) params.set('q', q); if (category) params.set('category', category);
    if (size) params.set('size', size); if (application) params.set('application', application);
    const canonical = baseUrl ? baseUrl + '/products' + (params.toString() ? '?' + params.toString() : '') : undefined;
    return {
      products: result.items, total: result.total, totalPages: result.totalPages, currentPage: result.page,
      categories, site, q: q || '', category: category || '', size: size || '', application: application || '',
      pageTitle: category ? category.replace(/-/g, ' ') + ' Wall Clocks | OSIRA' : 'Wall Clock Catalogue | OSIRA Jaipur',
      metaDescription: 'Browse OSIRA wall clocks by collection, size and application for retail, wholesale, corporate gifting and custom business orders.',
      canonical,
    };
  }

  @Get('products/:slug')
  @Render('product')
  async productPage(@Param('slug') slug: string) {
    const [product, related, site] = await Promise.all([
      this.products.findBySlug(slug), this.products.related(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const productUrl = baseUrl ? baseUrl + '/products/' + product.slug : '/products/' + product.slug;
    const schemaJsonLd = [{
      '@context':'https://schema.org','@type':'Product',name:product.name,description:product.shortDescription || product.description,
      image:product.image ? [product.image] : undefined,sku:product.sku || undefined,brand:{'@type':'Brand',name:product.brand || 'OSIRA'},
      category:product.category?.name,
      offers:product.price ? {'@type':'Offer',url:productUrl,priceCurrency:'INR',price:Number(product.price),availability:'https://schema.org/' + (product.availability === 'InStock' ? 'InStock' : 'PreOrder')} : undefined
    },{
      '@context':'https://schema.org','@type':'BreadcrumbList',
      itemListElement:[
        {'@type':'ListItem',position:1,name:'Home',item:baseUrl || '/'},{'@type':'ListItem',position:2,name:'Wall Clocks',item:(baseUrl || '')+'/products'},
        ...(product.category ? [{'@type':'ListItem',position:3,name:product.category.name,item:(baseUrl || '')+'/categories/'+product.category.slug}] : []),
        {'@type':'ListItem',position:product.category ? 4 : 3,name:product.name,item:productUrl}
      ]
    }];
    return {product,related,site,schemaJsonLd,pageTitle:product.metaTitle || product.name+' | OSIRA Wall Clocks',metaDescription:product.metaDescription || product.shortDescription || 'Explore '+product.name+' from OSIRA for retail, wholesale and business orders.',canonical:productUrl};
  }

  @Get('api/products')
  async productsApi(@Query('q') q?: string,@Query('category') category?: string,@Query('size') size?: string,@Query('application') application?: string,@Query('page') page='1') {
    return this.products.list(q,category,size,application,Number(page));
  }

  @Get('api/products/:slug')
  async productApi(@Param('slug') slug: string) { return this.products.findBySlug(slug); }
}
