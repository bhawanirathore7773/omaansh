import { Controller, Get, Param, Render } from '@nestjs/common';
import { BlogService } from './blog.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class BlogController {
  constructor(
    private readonly blog: BlogService,
    private readonly prisma: PrismaService,
  ) {}

  @Get('blog')
  @Render('blog')
  async listPage() {
    const [posts, site] = await Promise.all([
      this.blog.list(),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return {
      posts,
      site,
      pageTitle: 'Wall Clock Guides & Business Buying Resources | OSIRA',
      metaDescription: 'Practical wall clock buying guides, business ideas, customization information and sourcing resources from OSIRA.',
      canonical: baseUrl ? baseUrl + '/blog' : undefined,
    };
  }

  @Get('blog/:slug')
  @Render('blog-detail')
  async detailPage(@Param('slug') slug: string) {
    const [post, site] = await Promise.all([
      this.blog.findBySlug(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    const articleUrl = baseUrl ? baseUrl + '/blog/' + post.slug : '/blog/' + post.slug;
    const schemaJsonLd = [{
      '@context': 'https://schema.org',
      '@type': 'Article',
      headline: post.title,
      description: post.description,
      datePublished: post.createdAt,
      dateModified: post.updatedAt,
      mainEntityOfPage: articleUrl,
      publisher: { '@type': 'Organization', name: site?.businessName || 'OSIRA', url: baseUrl || undefined }
    },{
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Home', item: baseUrl || '/' },
        { '@type': 'ListItem', position: 2, name: 'Guides', item: (baseUrl || '') + '/blog' },
        { '@type': 'ListItem', position: 3, name: post.title, item: articleUrl }
      ]
    }];
    return {
      post,
      site,
      schemaJsonLd,
      pageTitle: post.metaTitle || post.title + ' | OSIRA',
      metaDescription: post.metaDescription || post.description.slice(0, 155),
      canonical: baseUrl ? baseUrl + '/blog/' + post.slug : undefined,
    };
  }

  @Get('api/blog')
  async apiList() { return this.blog.list(); }

  @Get('api/blog/:slug')
  async apiDetail(@Param('slug') slug: string) { return this.blog.findBySlug(slug); }
}
