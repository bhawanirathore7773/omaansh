import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { randomBytes, scryptSync, timingSafeEqual } from 'crypto';

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
  return require('crypto').createHash('sha256').update(value).digest('hex');
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
    const [products, categories, services, industries, cities, blogs, enquiries, newEnquiries] = await Promise.all([
      this.prisma.product.count({ where: { isActive: true } }),
      this.prisma.category.count(),
      this.prisma.servicePage.count({ where: { isPublished: true } }),
      this.prisma.industryPage.count({ where: { isPublished: true } }),
      this.prisma.cityPage.count({ where: { isPublished: true } }),
      this.prisma.blog.count({ where: { isPublished: true } }),
      this.prisma.enquiry.count(),
      this.prisma.enquiry.count({ where: { status: 'new' } }),
    ]);
    return { products, categories, services, industries, cities, blogs, enquiries, newEnquiries };
  }

  async recentEnquiries() {
    return this.prisma.enquiry.findMany({
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
