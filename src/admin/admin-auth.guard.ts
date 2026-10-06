import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';
import { Request } from 'express';
import { AdminService } from './admin.service';

function getCookie(req: Request, name: string) {
  const raw = req.headers.cookie || '';
  const part = raw.split(';').map(v => v.trim()).find(v => v.startsWith(name + '='));
  return part ? decodeURIComponent(part.slice(name.length + 1)) : undefined;
}

@Injectable()
export class AdminAuthGuard implements CanActivate {
  constructor(private readonly admin: AdminService) {}

  async canActivate(context: ExecutionContext) {
    const req = context.switchToHttp().getRequest<Request>();
    const session = await this.admin.getSession(getCookie(req, 'osira_admin'));
    if (!session) {
      if (req.path.startsWith('/admin/api')) throw new UnauthorizedException('Admin authentication required');
      const res = context.switchToHttp().getResponse();
      res.redirect(302, '/admin/login');
      return false;
    }
    (req as any).adminSession = session;
    (req as any).adminUser = session.user;
    (req as any).adminCsrf = getCookie(req, 'osira_admin_csrf');
    return true;
  }
}
