import { Body, Controller, Get, Param, Post, Query, Req, Res, UseGuards, UploadedFile, UseInterceptors, BadRequestException } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { mkdirSync } from 'fs';
import { extname, join } from 'path';
import { randomUUID } from 'crypto';
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
  @Get('products')
  async products(@Req() req: Request, @Res() res: Response) {
    const q = typeof req.query.q === 'string' ? req.query.q : '';
    return res.render('admin/products', { user: (req as any).adminUser, rows: await this.admin.listProductsAdmin(q), q });
  }

  @UseGuards(AdminAuthGuard)
  @Get('products/new')
  async newProduct(@Req() req: Request, @Res() res: Response) {
    const categories = await this.admin['prisma'].category.findMany({ orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }] });
    return res.render('admin/product-form', { user: (req as any).adminUser, product: null, categories, csrfToken: (req as any).adminCsrf });
  }

  @UseGuards(AdminAuthGuard)
  @Get('products/:id/edit')
  async editProduct(@Param('id') id: string, @Req() req: Request, @Res() res: Response) {
    const product = await this.admin.getProductAdmin(Number(id));
    if (!product) return res.status(404).send('Product not found');
    const categories = await this.admin['prisma'].category.findMany({ orderBy: [{ displayOrder: 'asc' }, { name: 'asc' }] });
    return res.render('admin/product-form', { user: (req as any).adminUser, product, categories, csrfToken: (req as any).adminCsrf });
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
  @Get('services')
  async services(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Services', kicker: 'SERVICES', description: 'Manage service pages.', rows: await this.admin.listServicesAdmin(), type: 'services', nameField: 'name' });
  }

  @UseGuards(AdminAuthGuard)
  @Get('industries')
  async industries(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Industries', kicker: 'INDUSTRIES', description: 'Manage industry landing pages.', rows: await this.admin.listIndustriesAdmin(), type: 'industries', nameField: 'industryName' });
  }

  @UseGuards(AdminAuthGuard)
  @Get('cities')
  async cities(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Cities', kicker: 'LOCAL SEO', description: 'Manage city landing pages.', rows: await this.admin.listCitiesAdmin(), type: 'cities', nameField: 'cityName' });
  }

  @UseGuards(AdminAuthGuard)
  @Get('blog')
  async blog(@Req() req: Request, @Res() res: Response) {
    return res.render('admin/content-list', { user: (req as any).adminUser, title: 'Blog', kicker: 'CONTENT', description: 'Manage SEO guides and articles.', rows: await this.admin.listBlogsAdmin(), type: 'blog', nameField: 'title' });
  }



  @UseGuards(AdminAuthGuard)
  @Post('banners/upload')
  @UseInterceptors(FileInterceptor('image', {
    storage: diskStorage({
      destination: (_req, _file, cb) => {
        const destination = join(process.cwd(), 'public', 'uploads', 'banners');
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
