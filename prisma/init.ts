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

  const [settings, categories, products, services, industries, cities, blogs, faqs, admins] = await Promise.all([
    prisma.siteSettings.count(), prisma.category.count(), prisma.product.count(),
    prisma.servicePage.count(), prisma.industryPage.count(), prisma.cityPage.count(),
    prisma.blog.count(), prisma.fAQ.count(), prisma.adminUser.count(),
  ]);
  const hasApplicationData = [categories, products, services, industries, cities, blogs, faqs, admins].some((count) => count > 0);
  if (!hasApplicationData) {
    console.log('OSIRA: fresh database detected. Running the initial seed once...');
    run('npx', ['prisma', 'db', 'seed']);
    console.log('OSIRA: initial seed completed.');
  } else {
    console.log('OSIRA: existing application data detected; seed skipped to protect production data.');
  }

  const adminEmail = process.env.ADMIN_EMAIL?.trim().toLowerCase();
  const adminPassword = process.env.ADMIN_PASSWORD;
  if (adminEmail && adminPassword && adminPassword !== 'CHANGE_THIS_TO_A_STRONG_PASSWORD') {
    const passwordHash = makeAdminHash(adminPassword);
    await prisma.adminUser.upsert({
      where: { email: adminEmail },
      update: { passwordHash, isActive: true, name: 'OSIRA Admin' },
      create: { email: adminEmail, name: 'OSIRA Admin', passwordHash, role: 'admin', isActive: true },
    });
    console.log('OSIRA: configured admin account synchronized for ' + adminEmail + '.');
  } else {
    console.log('OSIRA: ADMIN_EMAIL/ADMIN_PASSWORD missing; existing admin credentials unchanged.');
  }
}

main().catch((error) => {
  console.error('OSIRA Prisma initialization failed:', error);
  process.exitCode = 1;
}).finally(async () => {
  await prisma.$disconnect();
});
