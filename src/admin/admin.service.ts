import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { createHash, randomBytes, scryptSync, timingSafeEqual } from 'crypto';

function hashPassword(password: string) {
  const salt = randomBytes(16).toString('hex');
  const hash = scryptSync(password, salt, 64).toString('hex');
  return `scrypt$${salt}$${hash}`;
}

function verifyPassword(password: string, stored: string) {
  const [scheme, salt, hash] = stored.split('$');
  if (scheme !== 'scrypt' || !salt || !hash) return false;
  const derived = scryptSync(password, salt, 64);
  const expected = Buffer.from(hash, 'hex');
  return expected.length === derived.length && timingSafeEqual(expected, derived);
}

function sha256(value: string) {
  return createHash('sha256').update(value).digest('hex');
}

@Injectable()
export class AdminService {
  constructor(private readonly prisma: PrismaService) {}

  async login(email: string, password: string) {
    const user = await this.prisma.adminUser.findUnique({ where: { email: email.toLowerCase().trim() } });
    if (!user || !user.isActive || !verifyPassword(password, user.passwordHash)) {
      throw new UnauthorizedException('Invalid email or password');
    }

    await this.prisma.adminSession.deleteMany({ where: { userId: user.id, expiresAt: { lt: new Date() } } });

    const token = randomBytes(32).toString('hex');
    const csrfToken = randomBytes(32).toString('hex');
    const expiresAt = new Date(Date.now() + 1000 * 60 * 60 * 12);

    await this.prisma.adminSession.create({
      data: {
        tokenHash: sha256(token),
        csrfTokenHash: sha256(csrfToken),
        userId: user.id,
        expiresAt,
      },
    });

    return { token, csrfToken, expiresAt, user: { id: user.id, email: user.email, name: user.name, role: user.role } };
  }

  async cleanupExpiredSessions() {
    await this.prisma.adminSession.deleteMany({ where: { expiresAt: { lt: new Date() } } });
  }

  async getSession(token: string | undefined) {
    if (!token) return null;
    const session = await this.prisma.adminSession.findUnique({
      where: { tokenHash: sha256(token) },
      include: { user: true },
    });
    if (!session || session.expiresAt <= new Date() || !session.user.isActive) {
      if (session) await this.prisma.adminSession.delete({ where: { id: session.id } }).catch(() => undefined);
      return null;
    }
    return session;
  }

  async logout(token: string | undefined) {
    if (!token) return;
    await this.prisma.adminSession.deleteMany({ where: { tokenHash: sha256(token) } });
  }

  async verifyCsrf(sessionId: number, csrfToken: string | undefined) {
    if (!csrfToken) return false;
    const session = await this.prisma.adminSession.findUnique({ where: { id: sessionId } });
    return !!session && session.csrfTokenHash === sha256(csrfToken);
  }

  async dashboard() {
    const [products, categories, services, industries, cities, blogs, enquiries, newEnquiries, contactedEnquiries, quotedEnquiries, wonEnquiries] = await Promise.all([
      this.prisma.product.count({ where: { isActive: true } }),
      this.prisma.category.count(),
      this.prisma.servicePage.count({ where: { isPublished: true } }),
      this.prisma.industryPage.count({ where: { isPublished: true } }),
      this.prisma.cityPage.count({ where: { isPublished: true } }),
      this.prisma.blog.count({ where: { isPublished: true } }),
      this.prisma.enquiry.count(),
      this.prisma.enquiry.count({ where: { status: 'new' } }),
      this.prisma.enquiry.count({ where: { status: 'contacted' } }),
      this.prisma.enquiry.count({ where: { status: 'quoted' } }),
      this.prisma.enquiry.count({ where: { status: 'won' } }),
    ]);
    return { products, categories, services, industries, cities, blogs, enquiries, newEnquiries, contactedEnquiries, quotedEnquiries, wonEnquiries };
  }

  async recentEnquiries(status?: string) {
    const allowed = ['new', 'contacted', 'quoted', 'won', 'lost', 'closed'];
    const where = status && allowed.includes(status) ? { status } : {};
    return this.prisma.enquiry.findMany({
      where,
      include: { product: { select: { name: true } } },
      orderBy: { createdAt: 'desc' },
      take: 50,
    });
  }

  async updateEnquiryStatus(id: number, status: string, notes?: string) {
    const allowed = ['new', 'contacted', 'quoted', 'won', 'lost', 'closed'];
    if (!allowed.includes(status)) throw new Error('Invalid enquiry status');
    return this.prisma.enquiry.update({
      where: { id },
      data: { status, ...(notes !== undefined ? { notes } : {}) },
    });
  }

  async listServicesAdmin() { return this.prisma.servicePage.findMany({ orderBy: [{displayOrder:'asc'},{name:'asc'}] }); }
  async saveService(b:any,id?:number) {
    const data:any={name:String(b.name||'').trim(),slug:String(b.slug||'').trim().toLowerCase(),iconClass:b.iconClass||null,h1Heading:String(b.h1Heading||b.name||''),heroSubheading:b.heroSubheading||null,heroImage:b.heroImage||null,shortDescription:String(b.shortDescription||''),fullDescription:String(b.fullDescription||''),processContent:b.processContent||null,benefitsContent:b.benefitsContent||null,metaTitle:b.metaTitle||null,metaDescription:b.metaDescription||null,metaKeywords:b.metaKeywords||null,isPublished:b.isPublished==='on',displayOrder:Number(b.displayOrder||0)};
    return id?this.prisma.servicePage.update({where:{id},data}):this.prisma.servicePage.create({data});
  }
  async listIndustriesAdmin() { return this.prisma.industryPage.findMany({ orderBy:[{displayOrder:'asc'},{industryName:'asc'}] }); }
  async saveIndustry(b:any,id?:number) {
    const data:any={industryName:String(b.industryName||'').trim(),slug:String(b.slug||'').trim().toLowerCase(),iconClass:b.iconClass||null,h1Heading:String(b.h1Heading||b.industryName||''),heroSubheading:b.heroSubheading||null,heroImage:b.heroImage||null,introContent:String(b.introContent||''),benefitsContent:b.benefitsContent||null,customizationContent:b.customizationContent||null,caseStudyContent:b.caseStudyContent||null,metaTitle:b.metaTitle||null,metaDescription:b.metaDescription||null,metaKeywords:b.metaKeywords||null,isPublished:b.isPublished==='on',displayOrder:Number(b.displayOrder||0)};
    return id?this.prisma.industryPage.update({where:{id},data}):this.prisma.industryPage.create({data});
  }
  async listCitiesAdmin() { return this.prisma.cityPage.findMany({ orderBy:[{displayOrder:'asc'},{cityName:'asc'}] }); }
  async saveCity(b:any,id?:number) {
    const data:any={cityName:String(b.cityName||'').trim(),slug:String(b.slug||'').trim().toLowerCase(),state:b.state||null,pageType:b.pageType||'supplier',h1Heading:String(b.h1Heading||b.cityName||''),heroSubheading:b.heroSubheading||null,heroImage:b.heroImage||null,introContent:String(b.introContent||''),whyChooseContent:b.whyChooseContent||null,servicesContent:b.servicesContent||null,deliveryContent:b.deliveryContent||null,industriesContent:b.industriesContent||null,closingContent:b.closingContent||null,metaTitle:b.metaTitle||null,metaDescription:b.metaDescription||null,metaKeywords:b.metaKeywords||null,nearbyAreas:b.nearbyAreas||null,deliveryTime:b.deliveryTime||'3-5 business days',isPublished:b.isPublished==='on',displayOrder:Number(b.displayOrder||0)};
    return id?this.prisma.cityPage.update({where:{id},data}):this.prisma.cityPage.create({data});
  }
  async listBlogsAdmin() { return this.prisma.blog.findMany({ orderBy:{createdAt:'desc'} }); }
  async saveBlog(b:any,id?:number) {
    const data:any={title:String(b.title||'').trim(),slug:String(b.slug||'').trim().toLowerCase(),category:b.category||'Wall Clocks',featuredImage:b.featuredImage||null,description:String(b.description||''),contentHtml:b.contentHtml||null,inlineImage1:b.inlineImage1||null,inlineImage2:b.inlineImage2||null,inlineImage3:b.inlineImage3||null,inlineImage1Caption:b.inlineImage1Caption||null,inlineImage2Caption:b.inlineImage2Caption||null,inlineImage3Caption:b.inlineImage3Caption||null,metaTitle:b.metaTitle||null,metaDescription:b.metaDescription||null,metaKeywords:b.metaKeywords||null,isPublished:b.isPublished==='on'};
    return id?this.prisma.blog.update({where:{id},data}):this.prisma.blog.create({data});
  }
  async getSiteSettings() { return this.prisma.siteSettings.findUnique({where:{id:1}}); }
  async saveSiteSettings(b:any) {
    const data:any={businessName:b.businessName||'OSIRA',tagline:b.tagline||'',primaryPhone:b.primaryPhone||'',whatsappNumber:b.whatsappNumber||'',email:b.email||'',streetAddress:b.streetAddress||'',locality:b.locality||'',region:b.region||'',postalCode:b.postalCode||'',country:b.country||'IN',latitude:Number(b.latitude||0),longitude:Number(b.longitude||0),gstNumber:b.gstNumber||null,establishmentYear:Number(b.establishmentYear||2021),employeeCount:b.employeeCount||null,facebookUrl:b.facebookUrl||null,instagramUrl:b.instagramUrl||null,youtubeUrl:b.youtubeUrl||null,linkedinUrl:b.linkedinUrl||null,defaultMetaTitle:b.defaultMetaTitle||'OSIRA | Wall Clock Manufacturer & Supplier in Jaipur',defaultMetaDescription:b.defaultMetaDescription||'',googleVerification:b.googleVerification||null,bingVerification:b.bingVerification||null};
    return this.prisma.siteSettings.upsert({where:{id:1},update:data,create:{id:1,...data}});
  }

  async createAdminIfConfigured() {
    const email = process.env.ADMIN_EMAIL?.trim().toLowerCase();
    const password = process.env.ADMIN_PASSWORD;
    if (!email || !password || password === 'CHANGE_THIS_TO_A_STRONG_PASSWORD') return false;
    const existing = await this.prisma.adminUser.findUnique({ where: { email } });
    const passwordHash = hashPassword(password);
    if (existing) {
      await this.prisma.adminUser.update({ where: { id: existing.id }, data: { passwordHash, isActive: true } });
    } else {
      await this.prisma.adminUser.create({ data: { email, name: 'OSIRA Admin', passwordHash } });
    }
    return true;
  }
}
