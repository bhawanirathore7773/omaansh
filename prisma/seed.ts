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

  const services = [
    {
      name: 'Wholesale Wall Clocks',
      slug: 'wholesale-wall-clocks',
      h1Heading: 'Wholesale wall clocks for retailers and distributors',
      heroSubheading: 'Ready-to-sell wall clock designs with quantity-led pricing and business order support.',
      shortDescription: 'Source wall clocks for retail stores, dealers and distributors with practical MOQ and repeat-order support.',
      fullDescription: '<p>OSIRA supports wholesale buyers with a focused wall clock catalogue, quantity-led pricing and a straightforward enquiry process.</p>',
      processContent: '<ol><li>Share designs and required quantity.</li><li>Confirm pricing, packaging and delivery.</li><li>Approve the order and production plan.</li><li>Dispatch against the agreed schedule.</li></ol>',
      benefitsContent: '<p>Suitable for retailers, dealers and distributors looking for consistent designs, clear communication and repeat supply.</p>',
      metaTitle: 'Wholesale Wall Clocks Supplier | OSIRA Jaipur',
      metaDescription: 'Source wholesale wall clocks from OSIRA Jaipur for retailers, dealers and distributors.',
    },
    {
      name: 'Corporate Gifting',
      slug: 'corporate-gifting',
      h1Heading: 'Corporate gifting wall clocks with business branding',
      heroSubheading: 'Wall clocks for employee gifts, dealer programmes, milestones and institutional gifting.',
      shortDescription: 'Plan quantity-based gifting orders with branding, artwork and packaging requirements.',
      fullDescription: '<p>Turn a useful everyday product into a branded business gift. OSIRA can support corporate wall clock programmes around quantity, artwork and delivery requirements.</p>',
      processContent: '<ol><li>Share event, quantity and branding brief.</li><li>Review suitable product options.</li><li>Confirm artwork and commercial details.</li><li>Move into production and dispatch.</li></ol>',
      benefitsContent: '<p>Useful for employee recognition, dealer meets, anniversaries, launches and institutional programmes.</p>',
      metaTitle: 'Corporate Gifting Wall Clocks | OSIRA',
      metaDescription: 'Corporate gifting wall clocks with branding and quantity support from OSIRA Jaipur.',
    },
    {
      name: 'Promotional Branding',
      slug: 'promotional-branding',
      h1Heading: 'Promotional wall clocks for branded campaigns',
      heroSubheading: 'Put your logo, campaign artwork or business identity on a practical wall clock.',
      shortDescription: 'Promotional wall clocks for brands, dealers, distributors and marketing campaigns.',
      fullDescription: '<p>OSIRA supports promotional wall clock requirements where the product needs to carry a visible brand identity while remaining useful in homes, shops and workplaces.</p>',
      processContent: '<ol><li>Share logo, artwork and target quantity.</li><li>Discuss product and placement options.</li><li>Approve artwork and commercial terms.</li><li>Schedule production and dispatch.</li></ol>',
      benefitsContent: '<p>Suitable for dealer promotions, festive campaigns, product launches and brand visibility programmes.</p>',
      metaTitle: 'Promotional Wall Clocks | Custom Branding | OSIRA',
      metaDescription: 'Order promotional wall clocks with logo and campaign branding from OSIRA.',
    },
    {
      name: 'Custom OEM Manufacturing',
      slug: 'custom-oem-manufacturing',
      h1Heading: 'Custom wall clock manufacturing and OEM support',
      heroSubheading: 'Develop a wall clock around your dimensions, finish, branding and commercial requirement.',
      shortDescription: 'Custom and OEM wall clock support for product development, private-label and large business orders.',
      fullDescription: '<p>For custom or OEM projects, OSIRA can discuss the product direction, dimensions, finish, branding and quantity before production is planned.</p>',
      processContent: '<ol><li>Share the product brief or reference.</li><li>Review feasibility, materials and quantity.</li><li>Finalize sample or artwork requirements.</li><li>Confirm production and dispatch plan.</li></ol>',
      benefitsContent: '<p>Best suited to brands, importers, distributors and businesses that need a product adapted to a specific commercial brief.</p>',
      metaTitle: 'Custom OEM Wall Clock Manufacturer | OSIRA Jaipur',
      metaDescription: 'Custom and OEM wall clock manufacturing support for brands and business buyers in Jaipur.',
    },
  ];

  for (let i = 0; i < services.length; i++) {
    const service = services[i];
    await prisma.servicePage.upsert({
      where: { slug: service.slug },
      update: service,
      create: { ...service, displayOrder: i + 1 },
    });
  }

  console.log('OSIRA Prisma seed complete:', rows.length, 'catalogue rows processed');
}

main().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => prisma.$disconnect());
