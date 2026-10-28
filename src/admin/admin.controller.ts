import { Body, Controller, Get, Param, Post, Query, Req, Res, UseGuards, UploadedFile, UseInterceptors, BadRequestException } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { mkdirSync } from 'fs';
import { extname, join } from 'path';
import { randomUUID } from 'crypto';
import { uploadDirectory } from '../upload-storage';
import { Request, Response } from 'express';
import { AdminService } from './admin.service';
import { AdminAuthGuard } from './admin-auth.guard';

function getCookie(req: Request, name: string) {
  const raw = req.headers.cookie || '';
  const part = raw.split(';').map(v => v.trim()).find(v => v.startsWith(name + '='));
  return part ? decodeURIComponent(part.slice(name.length + 1)) : undefined;
}

function setCookie(res: Response, name: string, value: string, maxAge: number, httpOnly = true) {
  const secure = process.env.NODE_ENV === 'production' ? '; Secure' : '';
  res.append('Set-Cookie', `${name}=${encodeURIComponent(value)}; Max-Age=${maxAge}; Path=/; HttpOnly=${httpOnly ? 'true' : 'false'}; SameSite=Lax${secure}`);
}

function clearCookie(res: Response, name: string) {
  res.append('Set-Cookie', `${name}=; Max-Age=0; Path=/; HttpOnly=true; SameSite=Lax`);
}

@Controller('admin')
export class AdminController {
  constructor(private readonly admin: AdminService) {}

  @Get('login')
  loginPage(@Query('error') error: string | undefined, @Res() res: Response) {
    return res.render('admin/login', { error: error === '1' });
  }

  @Post('login')
  async login(@Body() body: { email?: string; password?: string }, @Res() res: Response) {
    try {
      const result = await this.admin.login(body.email || '', body.password || '');
      setCookie(res, 'osira_admin', result.token, 60 * 60 * 12, true);
      setCookie(res, 'osira_admin_csrf', result.csrfToken, 60 * 60 * 12, true);
      return res.redirect(303, '/admin');
    } catch {
      return res.redirect(303, '/admin/login?error=1');
    }
  }

  @Post('logout')
  async logout(@Req() req: Request, @Res() res: Response) {
    await this.admin.logout(getCookie(req, 'osira_admin'));
    clearCookie(res, 'osira_admin');
    clearCookie(res, 'osira_admin_csrf');
    return res.redirect(303, '/admin/login');
  }



  @UseGuards(AdminAuthGuard)
  @Post('products/upload-image')
  @UseInterceptors(FileInterceptor('image', {
    storage: diskStorage({
      destination: (_req, _file, cb) => {
        const destination = join(uploadDirectory, 'products');
        mkdirSync(destination, { recursive: true });
        cb(null, destination);
      },
      filename: (_req, file, cb) => cb(null, `${Date.now()}-${randomUUID()}${extname(file.originalname).toLowerCase()}`),
    }),
    limits: { fileSize: 8 * 1024 * 1024, files: 1 },
    fileFilter: (_req, file, cb) => {
      const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/avif'];
      if (!allowed.includes(file.mimetype)) return cb(new BadRequestException('Use JPG, PNG, WebP or AVIF image files.') as any, false);
      cb(null, true);
    },
  }))
  async uploadProductImage(@UploadedFile() file: Express.Multer.File, @Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).json({ error: 'Invalid CSRF token' });
    if (!file) return res.status(400).json({ error: 'Select a JPG, PNG, WebP or AVIF image up to 8 MB.' });
    return res.json({ url: `/uploads/products/${file.filename}` });
  }

  @UseGuards(AdminAuthGuard)
  @Get('home-sections')
  async homeProductSections(@Req() req: Request, @Res() res: Response) {
    const data = await this.admin.listHomeProductSectionsAdmin();
    return res.render('admin/home-sections', {
      user: (req as any).adminUser,
      csrfToken: (req as any).adminCsrf,
      sections: data.sections,
      products: data.products,
      saved: req.query.saved === '1',
    });
  }

  @UseGuards(AdminAuthGuard)
  @Post('home-sections/add')
  async addHomeProductSection(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    try {
      await this.admin.createHomeProductSection();
      return res.redirect(303, '/admin/home-sections');
    } catch (error) {
      return res.status(400).send(error instanceof Error ? error.message : 'Unable to add homepage section');
    }
  }

  @UseGuards(AdminAuthGuard)
  @Post('home-sections/save')
  async saveHomeProductSections(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    try {
      await this.admin.saveHomeProductSections(body);
      return res.redirect(303, '/admin/home-sections?saved=1');
    } catch (error) {
      return res.status(400).send(error instanceof Error ? error.message : 'Unable to save homepage product sections');
    }
  }

  @UseGuards(AdminAuthGuard)
  @Get('products')
  async products(@Req() req: Request, @Res() res: Response) {
    const q = typeof req.query.q === 'string' ? req.query.q : '';
    return res.render('admin/products', { user: (req as any).adminUser, csrfToken: (req as any).adminCsrf, rows: await this.admin.listProductsAdmin(q), q });
  }

  @UseGuards(AdminAuthGuard)
  @Get('products/new')
  async newProduct(@Req() req: Request, @Res() res: Response) {
    const categories = await this.admin.listCategoriesAdmin();
    return res.render('admin/product-form', { user: (req as any).adminUser, product: null, categories, csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Get('products/:id/edit')
  async editProduct(@Param('id') id: string, @Req() req: Request, @Res() res: Response) {
    const product = await this.admin.getProductAdmin(Number(id));
    if (!product) return res.status(404).send('Product not found');
    const categories = await this.admin.listCategoriesAdmin();
    return res.render('admin/product-form', { user: (req as any).adminUser, product, categories, csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Get('categories')
  async categories(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/categories', {
      user: (req as any).adminUser,
      csrfToken: (req as any).adminCsrf,
      rows: await this.admin.listCategoriesAdmin(),
    });
  }

  @UseGuards(AdminAuthGuard)
  @Get('categories/new')
  async newCategory(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/category-form', {
      user: (req as any).adminUser,
      category: null,
      csrfToken: (req as any).adminCsrf,
    });
  }

  @UseGuards(AdminAuthGuard)
  @Get('categories/:id/edit')
  async editCategory(@Param('id') id: string, @Req() req: Request, @Res() res: Response) {
    const category = await this.admin.getCategoryAdmin(Number(id));
    if (!category) return res.status(404).send('Collection not found');
    return res.render('admin/category-form', {
      user: (req as any).adminUser,
      category,
      csrfToken: (req as any).adminCsrf,
    });
  }

  @UseGuards(AdminAuthGuard)
  @Post('categories/save')
  async saveCategory(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    try {
      await this.admin.saveCategory(body, body.id ? Number(body.id) : undefined);
      return res.redirect(303, '/admin/categories');
    } catch (error) {
      return res.status(400).send(error instanceof Error ? error.message : 'Unable to save collection');
    }
  }

  @UseGuards(AdminAuthGuard)
  @Post('products/save')
  async saveProduct(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    try {
      await this.admin.saveProduct(body, body.id ? Number(body.id) : undefined);
      return res.redirect(303, '/admin/products');
    } catch (error) {
      return res.status(400).send(error instanceof Error ? error.message : 'Unable to save product');
    }
  }

  @UseGuards(AdminAuthGuard)
  @Post(':type/:id/delete')
  async deleteAdminRecord(@Param('type') type: string, @Param('id') id: string, @Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    const destinations: Record<string, string> = {
      products: '/admin/products', categories: '/admin/categories', services: '/admin/services',
      industries: '/admin/industries', cities: '/admin/cities', blog: '/admin/blog',
      'home-sections': '/admin/home-sections', banners: '/admin/banners',
      enquiries: '/admin/enquiries', 'reseller-materials': '/admin/reseller-materials',
    };
    if (!destinations[type]) return res.status(404).send('Delete action is not available for this section.');
    try {
      await this.admin.deleteAdminRecord(type, Number(id));
      return res.redirect(303, destinations[type] + '?deleted=1');
    } catch (error) {
      return res.status(400).send(error instanceof Error ? error.message : 'Unable to delete record.');
    }
  }

  private async renderContentEditor(type: 'services' | 'industries' | 'cities' | 'blog', id: number | null, req: Request, res: Response) {
    const configs: Record<string, any> = {
      services: {
        title: 'Service page', kicker: 'WEBSITE CONTENT',
        fields: [
          {name:'name',label:'Service name',required:true},{name:'slug',label:'URL slug',required:true,help:'Lowercase words separated by hyphens.'},
          {name:'iconClass',label:'Icon class',help:'Optional icon class used by the site.'},{name:'h1Heading',label:'Page H1 heading',required:true},
          {name:'heroSubheading',label:'Hero subheading',type:'textarea',rows:2},{name:'heroImage',label:'Hero image URL'},
          {name:'shortDescription',label:'Short description',type:'textarea',rows:3,required:true},{name:'fullDescription',label:'Full description',type:'textarea',rows:7,required:true},
          {name:'processContent',label:'Process content',type:'textarea',rows:5},{name:'benefitsContent',label:'Benefits content',type:'textarea',rows:5},
          {name:'metaTitle',label:'Meta title',maxlength:70},{name:'metaDescription',label:'Meta description',type:'textarea',rows:3,maxlength:160},{name:'metaKeywords',label:'Meta keywords'},
          {name:'displayOrder',label:'Display order',type:'number'},{name:'isPublished',label:'Published on website',type:'checkbox'}
        ]
      },
      industries: {
        title: 'Industry page', kicker: 'WEBSITE CONTENT',
        fields: [
          {name:'industryName',label:'Industry name',required:true},{name:'slug',label:'URL slug',required:true},{name:'iconClass',label:'Icon class'},
          {name:'h1Heading',label:'Page H1 heading',required:true},{name:'heroSubheading',label:'Hero subheading',type:'textarea',rows:2},{name:'heroImage',label:'Hero image URL'},
          {name:'introContent',label:'Introduction',type:'textarea',rows:6,required:true},{name:'benefitsContent',label:'Benefits',type:'textarea',rows:5},
          {name:'customizationContent',label:'Customization content',type:'textarea',rows:5},{name:'caseStudyContent',label:'Case study / examples',type:'textarea',rows:5},
          {name:'metaTitle',label:'Meta title',maxlength:70},{name:'metaDescription',label:'Meta description',type:'textarea',rows:3,maxlength:160},{name:'metaKeywords',label:'Meta keywords'},
          {name:'displayOrder',label:'Display order',type:'number'},{name:'isPublished',label:'Published on website',type:'checkbox'}
        ]
      },
      cities: {
        title: 'City landing page', kicker: 'LOCAL SEO',
        fields: [
          {name:'cityName',label:'City name',required:true},{name:'slug',label:'URL slug',required:true},{name:'state',label:'State / region'},
          {name:'pageType',label:'Page type',type:'select',options:[['supplier','Supplier'],['manufacturer','Manufacturer']]},{name:'h1Heading',label:'Page H1 heading',required:true},
          {name:'heroSubheading',label:'Hero subheading',type:'textarea',rows:2},{name:'heroImage',label:'Hero image URL'},
          {name:'introContent',label:'Introduction',type:'textarea',rows:6,required:true},{name:'whyChooseContent',label:'Why choose us',type:'textarea',rows:5},
          {name:'servicesContent',label:'Services / products',type:'textarea',rows:5},{name:'deliveryContent',label:'Delivery information',type:'textarea',rows:4},
          {name:'industriesContent',label:'Industries served',type:'textarea',rows:4},{name:'closingContent',label:'Closing CTA content',type:'textarea',rows:4},
          {name:'nearbyAreas',label:'Nearby areas (one per line)',type:'textarea',rows:3},{name:'deliveryTime',label:'Delivery estimate'},
          {name:'metaTitle',label:'Meta title',maxlength:70},{name:'metaDescription',label:'Meta description',type:'textarea',rows:3,maxlength:160},{name:'metaKeywords',label:'Meta keywords'},
          {name:'displayOrder',label:'Display order',type:'number'},{name:'isPublished',label:'Published on website',type:'checkbox'}
        ]
      },
      blog: {
        title: 'Blog article', kicker: 'CONTENT & SEO',
        fields: [
          {name:'title',label:'Article title',required:true},{name:'slug',label:'URL slug',required:true},{name:'category',label:'Category'},
          {name:'featuredImage',label:'Featured image URL'},{name:'description',label:'Excerpt / description',type:'textarea',rows:4,required:true},
          {name:'contentHtml',label:'Article content (HTML supported)',type:'textarea',rows:14,help:'Use clean headings, paragraphs, lists and links. Preview before publishing.'},
          {name:'inlineImage1',label:'Inline image 1 URL'},{name:'inlineImage1Caption',label:'Inline image 1 caption'},
          {name:'inlineImage2',label:'Inline image 2 URL'},{name:'inlineImage2Caption',label:'Inline image 2 caption'},
          {name:'inlineImage3',label:'Inline image 3 URL'},{name:'inlineImage3Caption',label:'Inline image 3 caption'},
          {name:'metaTitle',label:'Meta title',maxlength:70},{name:'metaDescription',label:'Meta description',type:'textarea',rows:3,maxlength:160},{name:'metaKeywords',label:'Meta keywords'},
          {name:'isPublished',label:'Published on website',type:'checkbox'}
        ]
      }
    };
    const config = configs[type];
    if (!config) return res.status(404).send('Content type not found');
    let rows: any[] = [];
    if (type === 'services') rows = await this.admin.listServicesAdmin();
    if (type === 'industries') rows = await this.admin.listIndustriesAdmin();
    if (type === 'cities') rows = await this.admin.listCitiesAdmin();
    if (type === 'blog') rows = await this.admin.listBlogsAdmin();
    const record = id === null ? null : rows.find((row) => row.id === id);
    if (id !== null && !record) return res.status(404).send('Content record not found');
    const availableProducts = type === 'services' ? await this.admin.listProductsAdmin() : [];
    return res.render('admin/content-form', {
      user: (req as any).adminUser, csrfToken: (req as any).adminCsrf,
      type, record, fields: config.fields, editorTitle: config.title,
      kicker: config.kicker, isNew: id === null, availableProducts,
    });
  }

  @UseGuards(AdminAuthGuard)
  @Get('services/new')
  async newService(@Req() req: Request, @Res() res: Response) { return this.renderContentEditor('services', null, req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('services/:id/edit')
  async editService(@Param('id') id: string, @Req() req: Request, @Res() res: Response) { return this.renderContentEditor('services', Number(id), req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('industries/new')
  async newIndustry(@Req() req: Request, @Res() res: Response) { return this.renderContentEditor('industries', null, req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('industries/:id/edit')
  async editIndustry(@Param('id') id: string, @Req() req: Request, @Res() res: Response) { return this.renderContentEditor('industries', Number(id), req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('cities/new')
  async newCity(@Req() req: Request, @Res() res: Response) { return this.renderContentEditor('cities', null, req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('cities/:id/edit')
  async editCity(@Param('id') id: string, @Req() req: Request, @Res() res: Response) { return this.renderContentEditor('cities', Number(id), req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('blog/new')
  async newBlog(@Req() req: Request, @Res() res: Response) { return this.renderContentEditor('blog', null, req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('blog/:id/edit')
  async editBlog(@Param('id') id: string, @Req() req: Request, @Res() res: Response) { return this.renderContentEditor('blog', Number(id), req, res); }

  @UseGuards(AdminAuthGuard)
  @Get('services')
  async services(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Services', kicker: 'SERVICES', description: 'Manage service pages.', rows: await this.admin.listServicesAdmin(), type: 'services', nameField: 'name', csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Get('industries')
  async industries(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Industries', kicker: 'INDUSTRIES', description: 'Manage industry landing pages.', rows: await this.admin.listIndustriesAdmin(), type: 'industries', nameField: 'industryName', csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Get('cities')
  async cities(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Cities', kicker: 'LOCAL SEO', description: 'Manage city landing pages.', rows: await this.admin.listCitiesAdmin(), type: 'cities', nameField: 'cityName', csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Get('blog')
  async blog(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Blog', kicker: 'CONTENT', description: 'Manage SEO guides and articles.', rows: await this.admin.listBlogsAdmin(), type: 'blog', nameField: 'title', csrfToken: (req as any).adminCsrf });
  }



  @UseGuards(AdminAuthGuard)
  @Post('banners/upload')
  @UseInterceptors(FileInterceptor('image', {
    storage: diskStorage({
      destination: (_req, _file, cb) => {
        const destination = join(uploadDirectory, 'banners');
        mkdirSync(destination, { recursive: true });
        cb(null, destination);
      },
      filename: (_req, file, cb) => cb(null, `${Date.now()}-${randomUUID()}${extname(file.originalname).toLowerCase()}`),
    }),
    limits: { fileSize: 8 * 1024 * 1024, files: 1 },
    fileFilter: (_req, file, cb) => {
      const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/avif'];
      if (!allowed.includes(file.mimetype)) return cb(new BadRequestException('Use JPG, PNG, WebP or AVIF image files.') as any, false);
      cb(null, true);
    },
  }))
  async uploadBannerImage(@UploadedFile() file: Express.Multer.File, @Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).json({ error: 'Invalid CSRF token' });
    if (!file) return res.status(400).json({ error: 'Select a JPG, PNG, WebP or AVIF image up to 8 MB.' });
    return res.json({ url: `/uploads/banners/${file.filename}` });
  }

  @UseGuards(AdminAuthGuard)
  @Post('banners/add')
  async addBanner(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    try {
      await this.admin.createHomeBanner();
      return res.redirect(303, '/admin/banners');
    } catch (error) {
      return res.status(400).send(error instanceof Error ? error.message : 'Unable to add slide');
    }
  }

  @UseGuards(AdminAuthGuard)
  @Get('banners')
  async banners(@Req() req: Request, @Res() res: Response) {
    const rows = await this.admin.listHomeBanners();
    return res.render('admin/banners', { user: (req as any).adminUser, rows, csrfToken: (req as any).adminCsrf, saved: req.query.saved === '1' });
  }

  @UseGuards(AdminAuthGuard)
  @Post('banners/save')
  async bannersSave(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    await this.admin.saveHomeBanners(body);
    return res.redirect(303, '/admin/banners?saved=1');
  }

  @UseGuards(AdminAuthGuard)
  @Get('reseller')
  async resellerAdmin(@Req() req: Request, @Res() res: Response) {
    const [settings, materials] = await Promise.all([
      this.admin.getResellerPageSettings(),
      this.admin.listResellerMaterialsAdmin(),
    ]);
    return res.render('admin/reseller', { user: (req as any).adminUser, settings, materials, csrfToken: (req as any).adminCsrf, saved: req.query.saved === '1' });
  }

  @UseGuards(AdminAuthGuard)
  @Post('reseller/settings/save')
  async saveResellerSettings(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    await this.admin.saveResellerPageSettings(body);
    return res.redirect(303, '/admin/reseller?saved=1');
  }

  @UseGuards(AdminAuthGuard)
  @Get('reseller-materials/new')
  async newResellerMaterial(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/reseller-material-form', { user: (req as any).adminUser, material: null, csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Get('reseller-materials/:id/edit')
  async editResellerMaterial(@Param('id') id: string, @Req() req: Request, @Res() res: Response) {
    const material = await this.admin.getResellerMaterialAdmin(Number(id));
    if (!material) return res.status(404).send('Reseller component not found');
    return res.render('admin/reseller-material-form', { user: (req as any).adminUser, material, csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Post('reseller-materials/save')
  async saveResellerMaterial(@Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).send('Invalid CSRF token');
    try {
      await this.admin.saveResellerMaterial(body, body.id ? Number(body.id) : undefined);
      return res.redirect(303, '/admin/reseller?saved=1');
    } catch (error) {
      return res.status(400).send(error instanceof Error ? error.message : 'Unable to save reseller component');
    }
  }

  @UseGuards(AdminAuthGuard)
  @Post('reseller-materials/upload-image')
  @UseInterceptors(FileInterceptor('image', {
    storage: diskStorage({
      destination: (_req, _file, cb) => {
        const destination = join(uploadDirectory, 'reseller-materials');
        mkdirSync(destination, { recursive: true });
        cb(null, destination);
      },
      filename: (_req, file, cb) => cb(null, `${Date.now()}-${randomUUID()}${extname(file.originalname).toLowerCase()}`),
    }),
    limits: { fileSize: 8 * 1024 * 1024, files: 1 },
    fileFilter: (_req, file, cb) => {
      const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/avif'];
      if (!allowed.includes(file.mimetype)) return cb(new BadRequestException('Use JPG, PNG, WebP or AVIF image files.') as any, false);
      cb(null, true);
    },
  }))
  async uploadResellerMaterialImage(@UploadedFile() file: Express.Multer.File, @Body() body: any, @Req() req: Request, @Res() res: Response) {
    const session = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(session.id, body.csrfToken))) return res.status(403).json({ error: 'Invalid CSRF token' });
    if (!file) return res.status(400).json({ error: 'Select a JPG, PNG, WebP or AVIF image up to 8 MB.' });
    return res.json({ url: `/uploads/reseller-materials/${file.filename}` });
  }

  @UseGuards(AdminAuthGuard)
  @UseGuards(AdminAuthGuard)
  @Get('settings')
  async settings(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/settings', { user: (req as any).adminUser, settings: await this.admin.getSiteSettings(), csrfToken: (req as any).adminCsrf, saved: req.query.saved === '1' });
  }

  @UseGuards(AdminAuthGuard)
  @Post('services/save')
  async serviceSave(@Body() b: any, @Req() req: Request, @Res() res: Response) {
    const s = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(s.id, b.csrfToken))) return res.status(403).send('Invalid CSRF token');
    await this.admin.saveService(b, b.id ? Number(b.id) : undefined);
    return res.redirect(303, '/admin/services');
  }

  @UseGuards(AdminAuthGuard)
  @Post('industries/save')
  async industrySave(@Body() b: any, @Req() req: Request, @Res() res: Response) {
    const s = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(s.id, b.csrfToken))) return res.status(403).send('Invalid CSRF token');
    await this.admin.saveIndustry(b, b.id ? Number(b.id) : undefined);
    return res.redirect(303, '/admin/industries');
  }

  @UseGuards(AdminAuthGuard)
  @Post('cities/save')
  async citySave(@Body() b: any, @Req() req: Request, @Res() res: Response) {
    const s = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(s.id, b.csrfToken))) return res.status(403).send('Invalid CSRF token');
    await this.admin.saveCity(b, b.id ? Number(b.id) : undefined);
    return res.redirect(303, '/admin/cities');
  }

  @UseGuards(AdminAuthGuard)
  @Post('blog/save')
  async blogSave(@Body() b: any, @Req() req: Request, @Res() res: Response) {
    const s = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(s.id, b.csrfToken))) return res.status(403).send('Invalid CSRF token');
    await this.admin.saveBlog(b, b.id ? Number(b.id) : undefined);
    return res.redirect(303, '/admin/blog');
  }

  @UseGuards(AdminAuthGuard)
  @UseGuards(AdminAuthGuard)
  @Post('settings/save')
  async settingsSave(@Body() b: any, @Req() req: Request, @Res() res: Response) {
    const s = (req as any).adminSession;
    if (!(await this.admin.verifyCsrf(s.id, b.csrfToken))) return res.status(403).send('Invalid CSRF token');
    await this.admin.saveSiteSettings(b);
    return res.redirect(303, '/admin/settings?saved=1');
  }

  @UseGuards(AdminAuthGuard)
  @Get()
  async dashboard(@Req() req: Request, @Res() res: Response) {
    await this.admin.cleanupExpiredSessions();
    const data = await this.admin.dashboard();
    return res.render('admin/dashboard', { user: (req as any).adminUser, data });
  }

  @UseGuards(AdminAuthGuard)
  @Get('enquiries')
  async enquiries(@Req() req: Request, @Res() res: Response) {
    const status = typeof req.query.status === 'string' ? req.query.status : undefined;
    const rows = await this.admin.recentEnquiries(status);
    return res.render('admin/enquiries', { user: (req as any).adminUser, rows, status: status || '', csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Post('enquiries/:id/status')
  async updateStatus(
    @Param('id') id: string,
    @Body() body: { status?: string; notes?: string; csrfToken?: string },
    @Req() req: Request,
    @Res() res: Response,
  ) {
    const session = (req as any).adminSession;
    const csrfOk = await this.admin.verifyCsrf(session.id, body.csrfToken);
    if (!csrfOk) return res.status(403).send('Invalid CSRF token');
    await this.admin.updateEnquiryStatus(Number(id), body.status || 'new', body.notes);
    return res.redirect(303, '/admin/enquiries');
  }
}
