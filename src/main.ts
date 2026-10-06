import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { join } from 'path';
import { Request, Response, NextFunction } from 'express';
import { AppModule } from './app.module';

const buckets = new Map<string, { count: number; resetAt: number }>();

function rateLimit(req: Request, res: Response, next: NextFunction) {
  if (req.method !== 'POST') return next();
  const protectedPath = req.path === '/enquiries' || req.path === '/admin/login';
  if (!protectedPath) return next();

  const now = Date.now();
  const windowMs = req.path === '/admin/login' ? 15 * 60 * 1000 : 60 * 60 * 1000;
  const max = req.path === '/admin/login' ? 10 : 5;
  const forwarded = req.headers['x-forwarded-for'];
  const ip = typeof forwarded === 'string' ? forwarded.split(',')[0].trim() : req.ip || 'unknown';
  const key = req.path + ':' + ip;
  const current = buckets.get(key);

  if (!current || current.resetAt <= now) {
    buckets.set(key, { count: 1, resetAt: now + windowMs });
    return next();
  }

  if (current.count >= max) {
    res.setHeader('Retry-After', Math.ceil((current.resetAt - now) / 1000));
    return res.status(429).send('Too many requests. Please try again later.');
  }

  current.count += 1;
  return next();
}

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(rateLimit);
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.setBaseViewsDir(join(__dirname, '..', 'views'));
  app.setViewEngine('ejs');
  app.useStaticAssets(join(__dirname, '..', 'public'), { prefix: '/' });
  app.useStaticAssets(join(__dirname, '..', 'static'), { prefix: '/static' });
  const port = Number(process.env.PORT || 3000);
  await app.listen(port, '0.0.0.0');
}
bootstrap();
