import { Body, Controller, Get, Param, Post, Query, Req, Res, UseGuards } from '@nestjs/common';
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
      setCookie(res, 'osira_admin_csrf', result.csrfToken, 60 * 60 * 12, false);
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
  @Get()
  async dashboard(@Req() req: Request, @Res() res: Response) {
    const data = await this.admin.dashboard();
    return res.render('admin/dashboard', { user: (req as any).adminUser, data });
  }

  @UseGuards(AdminAuthGuard)
  @Get('enquiries')
  async enquiries(@Req() req: Request, @Res() res: Response) {
    const rows = await this.admin.recentEnquiries();
    return res.render('admin/enquiries', { user: (req as any).adminUser, rows, csrfToken: (req as any).adminCsrf });
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
