import { PrismaClient } from '@prisma/client';
import { readFileSync } from 'fs';
import { join } from 'path';

const prisma = new PrismaClient();

function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];
    if (ch === '"' && quoted && next === '"') { field += '"'; i++; continue; }
    if (ch === '"') { quoted = !quoted; continue; }
    if (ch === ',' && !quoted) { row.push(field.trim()); field = ''; continue; }
    if ((ch === '\n' || ch === '\r') && !quoted) {
      if (ch === '\r' && next === '\n') i++;
      row.push(field.trim()); field = '';
      if (row.some(Boolean)) rows.push(row);
      row = [];
      continue;
    }
    field += ch;
  }
  if (field.length || row.length) { row.push(field.trim()); rows.push(row); }
  return rows;
}

function slugify(value: string) {
  return value.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

async function main() {
  await prisma.siteSettings.upsert({
    where: { id: 1 },
    update: { businessName: 'OSIRA', gstNumber: '08BVNPS9491J1ZG' },
    create: { id: 1, businessName: 'OSIRA', gstNumber: '08BVNPS9491J1ZG' },
  });

  const rows = parseCsv(readFileSync(join(process.cwd(), 'wall_clock_products.csv'), 'utf8'));
  const headers = rows.shift()!;
  const col = (name: string) => headers.indexOf(name);

  for (const name of [...new Set(rows.map(r => r[col('category')]).filter(Boolean))]) {
    await prisma.category.upsert({
      where: { slug: slugify(name) },
      update: {},
      create: { name, slug: slugify(name), description: 'Explore ' + name.toLowerCase() + ' wall clocks from OSIRA.' },
    });
  }

  for (const r of rows) {
    const name = r[col('product_name')];
    if (!name) continue;
    const categoryName = r[col('category')] || 'Wall Clocks';
    const category = await prisma.category.upsert({
      where: { slug: slugify(categoryName) },
      update: {},
      create: { name: categoryName, slug: slugify(categoryName), description: 'Explore ' + categoryName.toLowerCase() + ' wall clocks from OSIRA.' },
    });
    const images = [r[col('image_1')], r[col('image_2')], r[col('image_3')], r[col('image_4')]].filter(Boolean).map(v => '/static/images/products/' + v);
    await prisma.product.upsert({
      where: { slug: slugify(name) },
      update: {},
      create: {
        name,
        slug: slugify(name),
        categoryId: category.id,
        description: r[col('description')] || name,
        shortDescription: r[col('short_description')] || null,
        price: r[col('price')] ? Number(r[col('price')]) : null,
        moq: r[col('moq')] ? Number(r[col('moq')]) : 1,
        image: images[0] || null,
        additionalImages: images.slice(1),
        metaTitle: (r[col('meta_title')] || (name + ' | OSIRA')).slice(0, 70),
        metaDescription: (r[col('meta_description')] || r[col('description')] || name).slice(0, 160),
        metaKeywords: r[col('meta_keywords')] || null,
        isFeatured: (r[col('is_featured')] || '').toLowerCase() === 'yes',
        brand: 'OSIRA',
      },
    });
  }

  const defaultTier = await prisma.pricingTierTemplate.findUnique({ where: { name: 'Default' } });
  if (!defaultTier) {
    await prisma.pricingTierTemplate.create({ data: { name: 'Default' } });
  }
  console.log('OSIRA Prisma seed complete:', rows.length, 'catalogue rows processed');
}

main().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => prisma.$disconnect());
