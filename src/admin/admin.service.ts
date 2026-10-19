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


  async listCategoriesAdmin() {
    return this.prisma.category.findMany({
      include: { _count: { select: { products: true } } },
      orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }],
    });
  }

  async getCategoryAdmin(id: number) {
    return this.prisma.category.findUnique({ where: { id } });
  }

  async saveCategory(body: any, id?: number) {
    const name = String(body.name || '').trim();
    const slug = String(body.slug || '').trim().toLowerCase();
    if (!name || !slug) throw new Error('Collection name and slug are required.');
    const data: any = {
      name: name.slice(0, 200),
      slug: slug.slice(0, 220),
      description: String(body.description || '').trim(),
      image: String(body.image || '').trim().slice(0, 500) || null,
      staticImagePath: String(body.staticImagePath || '').trim().slice(0, 300) || null,
      h1Heading: String(body.h1Heading || '').trim().slice(0, 200) || null,
      displayOrder: Number.isFinite(Number(body.displayOrder)) ? Number(body.displayOrder) : 0,
      metaTitle: String(body.metaTitle || '').trim().slice(0, 70) || null,
      metaDescription: String(body.metaDescription || '').trim().slice(0, 160) || null,
      metaKeywords: String(body.metaKeywords || '').trim().slice(0, 300) || null,
      seoContent: String(body.seoContent || '').trim() || null,
      isFeatured: body.isFeatured === 'on' || body.isFeatured === true,
    };
    return id
      ? this.prisma.category.update({ where: { id }, data })
      : this.prisma.category.create({ data });
  }

  async listProductsAdmin(query?: string) {
    const q = String(query || '').trim();
    return this.prisma.product.findMany({
      where: q ? { OR: [{ name: { contains: q } }, { sku: { contains: q } }] } : {},
      include: { category: true },
      orderBy: [{ updatedAt: 'desc' }],
      take: 150,
    });
  }

  async getProductAdmin(id: number) {
    return this.prisma.product.findUnique({ where: { id }, include: { category: true } });
  }

  async saveProduct(body: any, id?: number) {
    const imageInput = body.additionalImages !== undefined ? body.additionalImages : [1, 2, 3, 4].map(i => body['additionalImage' + i]);
    const imageList = (Array.isArray(imageInput) ? imageInput : [imageInput]).map((value: any) => String(value || '').trim()).filter(Boolean).slice(0, 30);
    const specKeys = body.specKey === undefined ? [] : (Array.isArray(body.specKey) ? body.specKey : [body.specKey]);
    const specValues = body.specValue === undefined ? [] : (Array.isArray(body.specValue) ? body.specValue : [body.specValue]);
    const structuredSpecs = specKeys.map((key: any, index: number) => ({ key: String(key || '').trim(), value: String(specValues[index] || '').trim() })).filter((item: any) => item.key && item.value).map((item: any) => item.key + ': ' + item.value).join('\n');
    const specifications = structuredSpecs || String(body.specifications || '').trim();
    const data: any = {
      name: String(body.name || '').trim(),
      slug: String(body.slug || '').trim().toLowerCase(),
      categoryId: Number(body.categoryId),
      sku: String(body.sku || '').trim() || null,
      price: body.price !== undefined && String(body.price).trim() !== '' ? Number(body.price) : null,
      bulkPrice: body.bulkPrice !== undefined && String(body.bulkPrice).trim() !== '' ? Number(body.bulkPrice) : null,
      moq: Math.max(1, Number(body.moq || 1)),
      image: String(body.image || '').trim() || null,
      additionalImages: imageList,
      description: String(body.description || '').trim(),
      shortDescription: String(body.shortDescription || '').trim() || null,
      specifications: specifications || null,
      metaTitle: String(body.metaTitle || '').trim().slice(0, 70) || null,
      metaDescription: String(body.metaDescription || '').trim().slice(0, 160) || null,
      metaKeywords: String(body.metaKeywords || '').trim().slice(0, 300) || null,
      brand: String(body.brand || 'OSIRA').trim(),
      availability: body.availability === 'OutOfStock' ? 'OutOfStock' : 'InStock',
      isActive: body.isActive === 'on',
      isFeatured: body.isFeatured === 'on',
      isBestseller: body.isBestseller === 'on',
      isNewArrival: body.isNewArrival === 'on',
    };
    if (!data.name || !data.slug || !Number.isInteger(data.categoryId) || !data.description) throw new Error('Product name, slug, category and description are required.');
    // Only one product can own each merchandising slot. Selecting a new item
    // automatically clears the previous Featured / New Arrival assignment.
    if (data.isFeatured) await this.prisma.product.updateMany({ where: { isFeatured: true, ...(id ? { id: { not: id } } : {}) }, data: { isFeatured: false } });
    if (data.isNewArrival) await this.prisma.product.updateMany({ where: { isNewArrival: true, ...(id ? { id: { not: id } } : {}) }, data: { isNewArrival: false } });
    return id ? this.prisma.product.update({ where: { id }, data }) : this.prisma.product.create({ data });
  }

  async listServicesAdmin() { return this.prisma.servicePage.findMany({ orderBy: [{displayOrder:'asc'},{name:'asc'}] }); }
  async saveService(b:any,id?:number) {
    const selected = b.productIds === undefined ? [] : (Array.isArray(b.productIds) ? b.productIds : [b.productIds]);
    const productIds: number[] = Array.from(new Set<number>(selected.map((value: unknown) => Number(value)).filter((value: number) => Number.isInteger(value) && value > 0))).slice(0, 100);
    const validProducts = productIds.length ? await this.prisma.product.findMany({ where: { id: { in: productIds }, isActive: true }, select: { id: true } }) : [];
    const data:any={name:String(b.name||'').trim(),slug:String(b.slug||'').trim().toLowerCase(),iconClass:b.iconClass||null,h1Heading:String(b.h1Heading||b.name||''),heroSubheading:b.heroSubheading||null,heroImage:b.heroImage||null,shortDescription:String(b.shortDescription||''),fullDescription:String(b.fullDescription||''),processContent:b.processContent||null,benefitsContent:b.benefitsContent||null,productIds:validProducts.map(product=>product.id),metaTitle:b.metaTitle||null,metaDescription:b.metaDescription||null,metaKeywords:b.metaKeywords||null,isPublished:b.isPublished==='on',displayOrder:Number(b.displayOrder||0)};
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

  async ensureHomeProductSections() {
    const count = await this.prisma.homeProductSection.count();
    if (count === 0) {
      await this.prisma.homeProductSection.createMany({ data: [
        { title: 'New Arrivals', slug: 'new-arrivals', eyebrow: 'JUST ADDED', description: 'Explore the latest wall clock designs.', displayOrder: 1, isActive: true },
        { title: 'Best for Branding', slug: 'best-for-branding', eyebrow: 'CUSTOM & PROMOTIONAL', description: 'Wall clocks to consider for logo branding, campaigns and corporate gifting.', displayOrder: 2, isActive: true },
        { title: 'Best Sellers', slug: 'best-sellers', eyebrow: 'POPULAR CHOICES', description: 'Browse popular designs for retail, office and business orders.', displayOrder: 3, isActive: true },
        { title: 'Decorative Wall Clocks', slug: 'decorative-wall-clocks', eyebrow: 'DESIGNED FOR SPACES', description: 'Decorative options for homes, workplaces and reception areas.', displayOrder: 4, isActive: true },
        { title: 'Office & Corporate Clocks', slug: 'office-corporate-clocks', eyebrow: 'WORKPLACE FAVOURITES', description: 'Wall clocks for offices, institutions and corporate requirements.', displayOrder: 5, isActive: true },
      ], skipDuplicates: true });
    }
    return this.prisma.homeProductSection.findMany({
      orderBy: [{ displayOrder: 'asc' }, { id: 'asc' }],
      include: { products: { include: { product: { include: { category: true } } }, orderBy: { displayOrder: 'asc' } } },
    });
  }

  async listHomeProductSectionsAdmin() {
    await this.ensureHomeProductSections();
    const [sections, products] = await Promise.all([
      this.prisma.homeProductSection.findMany({
        orderBy: [{ displayOrder: 'asc' }, { id: 'asc' }],
        include: { products: { select: { productId: true } } },
      }),
      this.prisma.product.findMany({
        orderBy: [{ isActive: 'desc' }, { name: 'asc' }],
        include: { category: true },
      }),
    ]);
    return { sections, products };
  }

  async saveHomeProductSections(body: any) {
    const input = body?.sections;
    const rows = input ? (Array.isArray(input) ? input : [input]) : [];
    for (const row of rows.slice(0, 10)) {
      const id = Number(row.id);
      if (!Number.isInteger(id) || id < 1) continue;
      const title = String(row.title || '').trim().slice(0, 160);
      const slug = String(row.slug || '').trim().toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '').slice(0, 180);
      if (!title || !slug) throw new Error('Every section needs a title and URL slug.');
      const selected = row.productIds === undefined ? [] : (Array.isArray(row.productIds) ? row.productIds : [row.productIds]);
      const productIds: number[] = Array.from(new Set<number>(selected.map((value: unknown) => Number(value)).filter((value: number) => Number.isInteger(value) && value > 0)));
      const validProducts = productIds.length ? await this.prisma.product.findMany({ where: { id: { in: productIds } }, select: { id: true } }) : [];
      await this.prisma.$transaction(async tx => {
        await tx.homeProductSection.update({
          where: { id },
          data: {
            title,
            slug,
            eyebrow: String(row.eyebrow || '').trim().slice(0, 100) || null,
            description: String(row.description || '').trim().slice(0, 300) || null,
            displayOrder: Number.isFinite(Number(row.displayOrder)) ? Number(row.displayOrder) : id,
            isActive: row.isActive === 'on' || row.isActive === true,
          },
        });
        await tx.homeProductSectionItem.deleteMany({ where: { sectionId: id } });
        if (validProducts.length) await tx.homeProductSectionItem.createMany({
          data: validProducts.map((product, index) => ({ sectionId: id, productId: product.id, displayOrder: productIds.indexOf(product.id) >= 0 ? productIds.indexOf(product.id) : index })),
          skipDuplicates: true,
        });
      });
    }
  }

  async listHomeBanners() {
    return this.prisma.homeBanner.findMany({ orderBy: [{ displayOrder: 'asc' }, { id: 'asc' }] });
  }

  async createHomeBanner() {
    const count = await this.prisma.homeBanner.count();
    if (count >= 20) throw new Error('You can create up to 20 homepage slides.');
    return this.prisma.homeBanner.create({
      data: {
        title: 'OSIRA banner ' + (count + 1),
        displayOrder: count + 1,
        isActive: true,
        backgroundColor: '#17212b',
      },
    });
  }

  async saveHomeBanners(body: any) {
    const input = body?.banners;
    const rows = input ? (Array.isArray(input) ? input : [input]) : [];
    for (const row of rows.slice(0, 20)) {
      const id = Number(row.id);
      if (!Number.isInteger(id) || id < 1) continue;
      await this.prisma.homeBanner.update({
        where: { id },
        data: {
          title: String(row.title || '').trim().slice(0, 160) || ('OSIRA banner ' + id),
          subtitle: null,
          desktopImage: String(row.desktopImage || '').trim().slice(0, 700) || null,
          mobileImage: String(row.mobileImage || '').trim().slice(0, 700) || null,
          buttonLabel: null,
          linkUrl: null,
          backgroundColor: /^#[0-9a-fA-F]{6}$/.test(String(row.backgroundColor || '')) ? String(row.backgroundColor) : '#17212b',
          displayOrder: Number(row.displayOrder || id),
          isActive: row.isActive === 'on' || row.isActive === true,
        },
      });
    }
  }

  async getSiteSettings() { return this.prisma.siteSettings.findUnique({where:{id:1}}); }
  async saveSiteSettings(b:any) {
    const data:any={businessName:b.businessName||'OSIRA',tagline:b.tagline||'',primaryPhone:b.primaryPhone||'',whatsappNumber:b.whatsappNumber||'',email:b.email||'',streetAddress:b.streetAddress||'',locality:b.locality||'',region:b.region||'',postalCode:b.postalCode||'',country:b.country||'IN',latitude:Number(b.latitude||0),longitude:Number(b.longitude||0),gstNumber:b.gstNumber||null,establishmentYear:Number(b.establishmentYear||2021),employeeCount:b.employeeCount||null,facebookUrl:b.facebookUrl||null,instagramUrl:b.instagramUrl||null,youtubeUrl:b.youtubeUrl||null,linkedinUrl:b.linkedinUrl||null,indiamartUrl:b.indiamartUrl||null,defaultMetaTitle:b.defaultMetaTitle||'OSIRA | Wall Clock Manufacturer & Supplier in Jaipur',defaultMetaDescription:b.defaultMetaDescription||'',googleVerification:b.googleVerification||null,bingVerification:b.bingVerification||null};
    return this.prisma.siteSettings.upsert({where:{id:1},update:data,create:{id:1,...data}});
  }

  async getResellerPageSettings() {
    return this.prisma.resellerPageSettings.upsert({ where: { id: 1 }, update: {}, create: { id: 1 } });
  }

  async saveResellerPageSettings(body: any) {
    const text = (value: any, fallback = '') => String(value ?? fallback).trim();
    const data: any = {
      eyebrow: text(body.eyebrow, 'OSIRA RESELLER PROGRAMME').slice(0, 120),
      heroTitle: text(body.heroTitle).slice(0, 220),
      heroDescription: text(body.heroDescription),
      heroImage: text(body.heroImage).slice(0, 500) || null,
      introTitle: text(body.introTitle).slice(0, 220),
      introDescription: text(body.introDescription),
      qualityTitle: text(body.qualityTitle).slice(0, 220),
      qualityDescription: text(body.qualityDescription),
      whatsappIntro: text(body.whatsappIntro).slice(0, 5000),
      isPublished: body.isPublished === 'on' || body.isPublished === true,
    };
    return this.prisma.resellerPageSettings.upsert({ where: { id: 1 }, update: data, create: { id: 1, ...data } });
  }

  async listResellerMaterialsAdmin() {
    return this.prisma.resellerMaterial.findMany({ orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }] });
  }

  async getResellerMaterialAdmin(id: number) {
    return this.prisma.resellerMaterial.findUnique({ where: { id } });
  }

  async saveResellerMaterial(body: any, id?: number) {
    const text = (value: any) => String(value ?? '').trim();
    const list = (value: any) => text(value).split(/\r?\n|,/).map((item: string) => item.trim()).filter(Boolean).slice(0, 100);
    const jsonList = (value: any) => {
      try {
        const parsed = JSON.parse(text(value) || '[]');
        return Array.isArray(parsed) ? parsed.filter((item: any) => typeof item === 'string' && item.trim()).slice(0, 500) : [];
      } catch { return []; }
    };
    const specs = text(body.specificationsText).split(/\r?\n/).map((line: string) => {
      const at = line.indexOf(':');
      return at > 0 ? { key: line.slice(0, at).trim(), value: line.slice(at + 1).trim() } : null;
    }).filter((item: any) => item && item.key && item.value).slice(0, 50);
    const gallery = jsonList(body.galleryJson).map((url: string) => url.trim()).filter(Boolean);
    const slug = text(body.slug).toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 200);
    const name = text(body.name).slice(0, 180);
    if (!name || !slug) throw new Error('Component name and URL slug are required.');
    const data: any = {
      name, slug,
      componentType: text(body.componentType || 'Component').slice(0, 100),
      category: text(body.category || 'components').toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'components',
      isFeatured: body.isFeatured === 'on' || body.isFeatured === true,
      isRecommended: body.isRecommended === 'on' || body.isRecommended === true,
      shortDescription: text(body.shortDescription).slice(0, 300),
      description: text(body.description),
      image: text(body.image).slice(0, 500) || null,
      gallery: gallery as any,
      sizes: list(body.sizesText) as any,
      colors: list(body.colorsText) as any,
      styles: list(body.stylesText) as any,
      movementTypes: list(body.movementTypesText) as any,
      specifications: specs as any,
      qualityPoints: list(body.qualityPointsText) as any,
      orderingNotes: text(body.orderingNotes) || null,
      displayOrder: Number.isFinite(Number(body.displayOrder)) ? Number(body.displayOrder) : 0,
      isPublished: body.isPublished === 'on' || body.isPublished === true,
    };
    return id
      ? this.prisma.resellerMaterial.update({ where: { id }, data })
      : this.prisma.resellerMaterial.create({ data });
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
