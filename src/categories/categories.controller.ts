import { Controller, Get, Param, Render } from '@nestjs/common';
import { CategoriesService } from './categories.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class CategoriesController {
  constructor(private readonly categories: CategoriesService, private readonly prisma: PrismaService) {}

  @Get('categories')
  @Render('categories')
  async categoriesPage() {
    const [categories, site] = await Promise.all([
      this.categories.list(),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return {
      categories, site,
      pageTitle: 'Wall Clock Collections | OSIRA Jaipur',
      metaDescription: 'Explore OSIRA wall clock collections for retail, wholesale, corporate gifting, promotional and custom business orders.',
      canonical: baseUrl ? baseUrl + '/categories' : undefined,
    };
  }

  @Get('categories/:slug')
  @Render('category')
  async categoryPage(@Param('slug') slug: string) {
    const [category, site] = await Promise.all([
      this.categories.findBySlug(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const categoryUrl = baseUrl ? baseUrl + '/categories/' + category.slug : '/categories/' + category.slug;
    const schemaJsonLd = [
      {
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        name: category.h1Heading || category.name,
        description: category.metaDescription || category.description,
        url: categoryUrl
      },
      {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: baseUrl || '/' },
          { '@type': 'ListItem', position: 2, name: 'Collections', item: (baseUrl || '') + '/categories' },
          { '@type': 'ListItem', position: 3, name: category.name, item: categoryUrl }
        ]
      }
    ];
    return {
      category, site, schemaJsonLd,
      pageTitle: category.metaTitle || category.name + ' Wall Clocks | OSIRA Jaipur',
      metaDescription: category.metaDescription || category.description || 'Explore ' + category.name + ' wall clocks from OSIRA.',
      canonical: baseUrl ? baseUrl + '/categories/' + category.slug : undefined,
    };
  }

  @Get('api/categories')
  async categoriesApi() { return this.categories.list(); }

  @Get('api/categories/:slug')
  async categoryApi(@Param('slug') slug: string) { return this.categories.findBySlug(slug); }
}
