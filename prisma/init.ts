import { execFileSync } from 'child_process';
import { randomBytes, scryptSync } from 'crypto';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();
function run(command: string, args: string[]) {
  const executable = process.platform === 'win32' && command === 'npx' ? 'npx.cmd' : command;
  execFileSync(executable, args, { stdio: 'inherit', env: process.env });
}
function makeAdminHash(password: string) {
  const salt = randomBytes(16).toString('hex');
  const digest = scryptSync(password, salt, 64).toString('hex');
  return ['scrypt', salt, digest].join(String.fromCharCode(36));
}
async function main() {
  if (!process.env.DATABASE_URL) throw new Error('DATABASE_URL is required before Prisma initialization.');
  console.log('OSIRA: synchronizing Prisma schema...');
  run('npx', ['prisma', 'db', 'push', '--skip-generate']);
  const [categories, products, services, industries, cities, blogs, faqs, admins] = await Promise.all([
    prisma.category.count(), prisma.product.count(), prisma.servicePage.count(), prisma.industryPage.count(),
    prisma.cityPage.count(), prisma.blog.count(), prisma.fAQ.count(), prisma.adminUser.count(),
  ]);
  const hasData = [categories, products, services, industries, cities, blogs, faqs, admins].some((n) => n > 0);
  if (!hasData) {
    console.log('OSIRA: fresh database detected; running initial seed.');
    run('npx', ['prisma', 'db', 'seed']);
  } else {
    console.log('OSIRA: existing application data detected; seed skipped.');
  }
  const email = process.env.ADMIN_EMAIL?.trim().toLowerCase();
  const password = process.env.ADMIN_PASSWORD;
  if (email && password && password !== 'CHANGE_THIS_TO_A_STRONG_PASSWORD') {
    const passwordHash = makeAdminHash(password);
    await prisma.adminUser.upsert({
      where: { email },
      update: { passwordHash, isActive: true, name: 'OSIRA Admin' },
      create: { email, name: 'OSIRA Admin', passwordHash, role: 'admin', isActive: true },
    });
    console.log('OSIRA: configured admin account synchronized for ' + email + '.');
  } else {
    console.log('OSIRA: admin environment variables missing; credentials unchanged.');
  }
}
main().catch((error) => {
  console.error('OSIRA Prisma initialization failed:', error);
  process.exitCode = 1;
}).finally(async () => {
  await prisma.$disconnect();
});
