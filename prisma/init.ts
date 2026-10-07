import { execFileSync } from 'child_process';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

function run(command: string, args: string[]) {
  const executable = process.platform === 'win32' && command === 'npx' ? 'npx.cmd' : command;
  execFileSync(executable, args, {
    stdio: 'inherit',
    env: process.env,
  });
}

async function main() {
  if (!process.env.DATABASE_URL) {
    throw new Error('DATABASE_URL is required before Prisma initialization.');
  }

  console.log('OSIRA: synchronizing Prisma schema...');
  run('npx', ['prisma', 'db', 'push', '--skip-generate']);

  const [settings, categories, products, services, industries, cities, blogs, faqs, admins] =
    await Promise.all([
      prisma.siteSettings.count(),
      prisma.category.count(),
      prisma.product.count(),
      prisma.servicePage.count(),
      prisma.industryPage.count(),
      prisma.cityPage.count(),
      prisma.blog.count(),
      prisma.fAQ.count(),
      prisma.adminUser.count(),
    ]);

  const contentCounts = [categories, products, services, industries, cities, blogs, faqs, admins];
  const hasApplicationData = contentCounts.some((count) => count > 0);

  if (!hasApplicationData) {
    console.log('OSIRA: fresh database detected. Running the initial seed once...');
    run('npx', ['prisma', 'db', 'seed']);
    console.log('OSIRA: initial seed completed.');
  } else {
    console.log(
      `OSIRA: existing application data detected (settings=${settings}, categories=${categories}, products=${products}, services=${services}, industries=${industries}, cities=${cities}, blogs=${blogs}, faqs=${faqs}, admins=${admins}). Seed skipped to protect production data.`,
    );
  }
}

main()
  .catch((error) => {
    console.error('OSIRA Prisma initialization failed:', error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
