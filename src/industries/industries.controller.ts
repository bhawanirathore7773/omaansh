import { Controller, Get, Param, Render } from '@nestjs/common';
import { IndustriesService } from './industries.service';
import { PrismaService } from '../prisma/prisma.service';

@Controller()
export class IndustriesController {
  constructor(
    private readonly industries: IndustriesService,
    private readonly prisma: PrismaService,
  ) {}

  @Get('industries')
  @Render('industries')
  async listPage() {
    const [industries, site] = await Promise.all([
      this.industries.list(),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return {
      industries,
      site,
      pageTitle: 'Wall Clocks for Industries | Corporate & Commercial Supply | OSIRA',
      metaDescription: 'Explore OSIRA wall clock solutions for hotels, offices, retail, education, healthcare and other commercial environments.',
      canonical: baseUrl ? baseUrl + '/industries' : undefined,
    };
  }

  @Get('industries/:slug')
  @Render('industry')
  async detailPage(@Param('slug') slug: string) {
    const [industry, site] = await Promise.all([
      this.industries.findBySlug(slug),
      this.prisma.siteSettings.findUnique({ where: { id: 1 } }),
    ]);
    const baseUrl = (process.env.SITE_URL || '').replace(/\/$/, '');
    return {
      industry,
      site,
      pageTitle: industry.metaTitle || industry.industryName + ' Wall Clocks | OSIRA',
      metaDescription: industry.metaDescription || industry.heroSubheading || industry.introContent.slice(0, 155),
      canonical: baseUrl ? baseUrl + '/industries/' + industry.slug : undefined,
    };
  }

  @Get('api/industries')
  async apiList() { return this.industries.list(); }

  @Get('api/industries/:slug')
  async apiDetail(@Param('slug') slug: string) { return this.industries.findBySlug(slug); }
}
