import { PrismaClient } from '@prisma/client';
import { readFileSync } from 'fs';
import { randomBytes, scryptSync } from 'crypto';
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

function hashPassword(password: string) {
  const salt = randomBytes(16).toString('hex');
  const hash = scryptSync(password, salt, 64).toString('hex');
  return `scrypt${salt}${hash}`;
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

  // SEO collection pages are represented by curated categories so each landing page
  // has a distinct search intent instead of creating duplicate keyword-only URLs.
  const seoCollections = [
    ['8-inch-wall-clocks', '8 Inch Wall Clocks', 'Compact 8 inch wall clocks for homes, offices, retail counters and gifting.'],
    ['10-inch-wall-clocks', '10 Inch Wall Clocks', '10 inch wall clocks for everyday home, office, retail and institutional use.'],
    ['12-inch-wall-clocks', '12 Inch Wall Clocks', '12 inch wall clocks for clear readability and practical commercial spaces.'],
    ['14-inch-wall-clocks', '14 Inch Wall Clocks', '14 inch wall clocks for larger walls, offices, halls and commercial interiors.'],
    ['plastic-wall-clocks', 'Plastic Wall Clocks', 'Plastic wall clocks covering practical, decorative and promotional buying requirements.'],
    ['designer-wall-clocks', 'Designer Wall Clocks', 'Designer wall clocks for contemporary interiors, décor stores and premium spaces.'],
    ['decorative-wall-clocks', 'Decorative Wall Clocks', 'Decorative wall clocks for homes, hospitality spaces, offices and gifting.'],
    ['promotional-wall-clocks', 'Promotional Wall Clocks', 'Promotional wall clocks for branded corporate gifting, campaigns and bulk orders.'],
    ['custom-wall-clocks', 'Custom Wall Clocks', 'Custom wall clocks for logos, branding, colour requirements and business orders.'],
    ['square-rectangle-wall-clocks', 'Square & Rectangle Wall Clocks', 'Square and rectangular wall clocks for modern interiors and commercial spaces.'],
  ];
  for (const [slug, name, description] of seoCollections) {
    await prisma.category.upsert({
      where: { slug },
      update: {
        description,
        metaTitle: (name + ' | OSIRA Jaipur').slice(0, 70),
        metaDescription: (description + ' Wholesale and business enquiries from OSIRA.').slice(0, 160),
        h1Heading: name,
        seoContent: '<p>' + description + ' Explore available OSIRA designs, specifications and business-order options before requesting a quotation.</p>',
      },
      create: {
        name,
        slug,
        description,
        metaTitle: (name + ' | OSIRA Jaipur').slice(0, 70),
        metaDescription: (description + ' Wholesale and business enquiries from OSIRA.').slice(0, 160),
        h1Heading: name,
        seoContent: '<p>' + description + ' Explore available OSIRA designs, specifications and business-order options before requesting a quotation.</p>',
        displayOrder: 20,
      },
    });
  }

  // Import the market-research catalogue as unpublished draft products.
  // These records are research variants, not verified OSIRA inventory; admin must verify
  // actual design, price, MOQ and images before activating them for public SEO.
  const marketPath = join(process.cwd(), 'data', 'market_researched_products.csv');
  try {
    const marketRows = parseCsv(readFileSync(marketPath, 'utf8'));
    const marketHeaders = marketRows.shift()!;
    const mcol = (name: string) => marketHeaders.indexOf(name);
    for (const r of marketRows) {
      const name = r[mcol('name')];
      const categoryName = r[mcol('category')];
      if (!name || !categoryName) continue;
      const category = await prisma.category.upsert({
        where: { slug: r[mcol('slug')] || slugify(categoryName) },
        update: {
          metaTitle: (categoryName + ' | OSIRA').slice(0, 70),
          metaDescription: ('Explore ' + categoryName.toLowerCase() + ' for wholesale, retail and business orders from OSIRA.').slice(0, 160),
        },
        create: {
          name: categoryName,
          slug: r[mcol('slug')] || slugify(categoryName),
          description: r[mcol('description')] || ('Explore ' + categoryName.toLowerCase() + ' from OSIRA.'),
          metaTitle: (categoryName + ' | OSIRA').slice(0, 70),
          metaDescription: ('Explore ' + categoryName.toLowerCase() + ' for wholesale, retail and business orders from OSIRA.').slice(0, 160),
          h1Heading: categoryName,
          seoContent: '<p>Market-researched category for wall clock buyers. Confirm current designs, specifications, MOQ and commercial pricing before ordering.</p>',
        },
      });
      await prisma.product.upsert({
        where: { slug: r[mcol('product_slug')] },
        update: {
          categoryId: category.id,
          availability: 'Research',
          isActive: false,
          metaTitle: (r[mcol('meta_title')] || name).slice(0, 70),
          metaDescription: (r[mcol('meta_description')] || r[mcol('description')] || name).slice(0, 160),
          metaKeywords: r[mcol('secondary_keywords')] || null,
        },
        create: {
          name,
          slug: r[mcol('product_slug')],
          categoryId: category.id,
          description: r[mcol('description')] || name,
          shortDescription: r[mcol('h1')] || name,
          specifications: [
            'Size: ' + (r[mcol('size')] || 'Confirm'),
            'Material: ' + (r[mcol('material')] || 'Confirm'),
            'Shape: ' + (r[mcol('shape')] || 'Confirm'),
            'Movement: ' + (r[mcol('movement')] || 'Confirm'),
            'Finish: ' + (r[mcol('finish')] || 'Confirm'),
            'Colours: ' + (r[mcol('color_options')] || 'Confirm'),
            'MOQ: ' + (r[mcol('moq')] || 'Confirm'),
          ].join('\n'),
          price: r[mcol('price_inr')] ? Number(r[mcol('price_inr')]) : null,
          moq: r[mcol('moq')] ? Number(r[mcol('moq')]) : 1,
          metaTitle: (r[mcol('meta_title')] || name).slice(0, 70),
          metaDescription: (r[mcol('meta_description')] || r[mcol('description')] || name).slice(0, 160),
          metaKeywords: r[mcol('secondary_keywords')] || null,
          brand: 'OSIRA',
          availability: 'Research',
          isActive: false,
        },
      });
    }
  } catch {
    // The research CSV is optional during local development.
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


  const industries = [
    {
      industryName: 'Hotels & Hospitality',
      slug: 'hotels-hospitality',
      iconClass: 'HOSPITALITY',
      h1Heading: 'Wall clocks for hotels and hospitality spaces',
      heroSubheading: 'Coordinate practical timekeeping with room aesthetics, common areas and brand identity.',
      introContent: '<p>OSIRA wall clocks can support hotel rooms, reception areas, lounges, restaurants and back-office spaces where clear timekeeping and visual consistency matter.</p>',
      benefitsContent: '<p>Choose designs around the interior style, viewing distance, placement and quantity required across multiple locations.</p>',
      customizationContent: '<p>Business buyers can discuss branding, finishes, dimensions and quantity-led requirements before placing an order.</p>',
      caseStudyContent: '<p>Suitable for hotel chains, boutique properties, resorts, restaurants and hospitality projects.</p>',
      metaTitle: 'Hotel Wall Clocks Supplier | OSIRA',
      metaDescription: 'Wall clocks for hotels, resorts and hospitality spaces with business-order support from OSIRA.',
    },
    {
      industryName: 'Corporate Offices',
      slug: 'corporate-offices',
      iconClass: 'OFFICES',
      h1Heading: 'Wall clocks for corporate offices and workplaces',
      heroSubheading: 'Professional wall clocks for meeting rooms, cabins, reception areas and shared workplaces.',
      introContent: '<p>OSIRA supplies wall clocks for offices where readability, design and consistent placement are part of the workplace environment.</p>',
      benefitsContent: '<p>Use a consistent design language across departments, floors or multiple office locations.</p>',
      customizationContent: '<p>Discuss logo placement, finishes and quantities for corporate projects, office openings and employee programmes.</p>',
      caseStudyContent: '<p>Useful for headquarters, branches, coworking spaces, training centres and institutional offices.</p>',
      metaTitle: 'Office Wall Clocks Supplier | OSIRA Jaipur',
      metaDescription: 'Professional wall clocks for offices, meeting rooms and corporate workplaces.',
    },
    {
      industryName: 'Retail Stores',
      slug: 'retail-stores',
      iconClass: 'RETAIL',
      h1Heading: 'Wall clocks for retail stores and dealer networks',
      heroSubheading: 'Retail-ready wall clocks for stores, showrooms, dealers and distribution networks.',
      introContent: '<p>Retail buyers can source wall clocks around design demand, selling price, MOQ and repeat availability.</p>',
      benefitsContent: '<p>Build a practical assortment for stores with a mix of modern, minimal and statement designs.</p>',
      customizationContent: '<p>Promotional and branded programmes can be planned for dealer networks and seasonal campaigns.</p>',
      caseStudyContent: '<p>Suitable for home décor retailers, furniture stores, lifestyle shops and multi-location dealer networks.</p>',
      metaTitle: 'Retail Wall Clocks Supplier | OSIRA',
      metaDescription: 'Source retail wall clocks for stores, showrooms and dealer networks from OSIRA.',
    },
    {
      industryName: 'Education',
      slug: 'education',
      iconClass: 'EDUCATION',
      h1Heading: 'Wall clocks for schools, colleges and education spaces',
      heroSubheading: 'Clear, dependable wall clocks for classrooms, corridors, offices and common areas.',
      introContent: '<p>Educational institutions need easy-to-read clocks across classrooms, administration areas, laboratories and common spaces.</p>',
      benefitsContent: '<p>Prioritize clear viewing, practical placement and consistent supply across buildings or campuses.</p>',
      customizationContent: '<p>Institutional and branded requirements can be discussed for larger programmes and campus projects.</p>',
      caseStudyContent: '<p>Suitable for schools, colleges, coaching centres, training institutes and campus facilities.</p>',
      metaTitle: 'School & College Wall Clocks | OSIRA',
      metaDescription: 'Wall clocks for schools, colleges, coaching centres and educational institutions.',
    },
    {
      industryName: 'Healthcare',
      slug: 'healthcare',
      iconClass: 'HEALTHCARE',
      h1Heading: 'Wall clocks for hospitals and healthcare facilities',
      heroSubheading: 'Readable wall clocks for clinics, hospitals, waiting areas and staff spaces.',
      introContent: '<p>Healthcare environments benefit from simple, highly visible timekeeping across reception, waiting areas, offices and staff spaces.</p>',
      benefitsContent: '<p>Choose practical designs that remain easy to read without competing with the surrounding environment.</p>',
      customizationContent: '<p>Quantity and institutional branding requirements can be planned for new facilities or refurbishment projects.</p>',
      caseStudyContent: '<p>Suitable for hospitals, clinics, diagnostic centres, pharmacies and healthcare offices.</p>',
      metaTitle: 'Hospital Wall Clocks Supplier | OSIRA',
      metaDescription: 'Readable wall clocks for hospitals, clinics and healthcare facilities from OSIRA.',
    },
    {
      industryName: 'Residential Projects',
      slug: 'residential-projects',
      iconClass: 'RESIDENTIAL',
      h1Heading: 'Wall clocks for residential projects and home décor',
      heroSubheading: 'Design-led wall clocks for homes, apartments, interior projects and décor programmes.',
      introContent: '<p>OSIRA offers wall clocks for living rooms, bedrooms, dining areas, work-from-home spaces and residential interior projects.</p>',
      benefitsContent: '<p>Choose styles that balance readability with the visual character of the room and overall décor.</p>',
      customizationContent: '<p>Interior designers and project buyers can discuss quantities, coordinated designs and custom requirements.</p>',
      caseStudyContent: '<p>Suitable for builders, interior designers, home décor retailers and residential project procurement.</p>',
      metaTitle: 'Residential Wall Clocks | Home Décor Supplier | OSIRA',
      metaDescription: 'Wall clocks for homes, interior designers and residential projects from OSIRA.',
    },
  ];

  for (let i = 0; i < industries.length; i++) {
    const industry = industries[i];
    await prisma.industryPage.upsert({
      where: { slug: industry.slug },
      update: industry,
      create: { ...industry, displayOrder: i + 1 },
    });
  }

  const cities = [
    {
      cityName: 'Jaipur',
      slug: 'jaipur',
      state: 'Rajasthan',
      pageType: 'supplier',
      h1Heading: 'Wall Clock Manufacturer & Supplier in Jaipur',
      heroSubheading: 'Source wall clocks in Jaipur for retail, wholesale, corporate gifting and custom business requirements.',
      introContent: '<p>OSIRA serves Jaipur buyers looking for wall clocks for homes, offices, stores, hospitality projects and business programmes.</p>',
      whyChooseContent: '<p>Local business buyers can discuss designs, quantities, branding, delivery and repeat supply with a Jaipur-based team.</p>',
      servicesContent: '<p>Wholesale supply, corporate gifting, promotional branding and custom/OEM requirements are supported through a direct enquiry process.</p>',
      deliveryContent: '<p>Delivery timelines depend on product, quantity and destination. Confirm the schedule before ordering.</p>',
      industriesContent: '<p>Common requirements include retail stores, offices, hotels, schools, healthcare facilities and residential projects.</p>',
      closingContent: '<p>Share your design preference, quantity and delivery requirement to receive a suitable recommendation.</p>',
      metaTitle: 'Wall Clock Manufacturer in Jaipur | OSIRA',
      metaDescription: 'OSIRA wall clock manufacturer and supplier in Jaipur for wholesale, custom and business orders.',
      nearbyAreas: 'Gokulpura, Kalwar Road, Vaishali Nagar, Jhotwara, Mansarovar, Ajmer Road and nearby Jaipur areas.',
      deliveryTime: '3-5 business days',
    },
    {
      cityName: 'Delhi',
      slug: 'delhi',
      state: 'Delhi',
      pageType: 'supplier',
      h1Heading: 'Wall Clock Supplier in Delhi for Business Orders',
      heroSubheading: 'Wholesale and custom wall clock supply for retailers, offices and commercial projects in Delhi.',
      introContent: '<p>Businesses in Delhi can source OSIRA wall clocks for retail, gifting, promotional and commercial requirements.</p>',
      whyChooseContent: '<p>Choose from an active catalogue and share quantity, branding and delivery details for a business quotation.</p>',
      servicesContent: '<p>Wholesale, corporate gifting, promotional branding and custom requirements are available.</p>',
      deliveryContent: '<p>Delivery depends on product availability, quantity and destination. Confirm the schedule with the team.</p>',
      industriesContent: '<p>Suitable for retail, offices, hospitality, education, healthcare and residential projects.</p>',
      closingContent: '<p>Send your requirement to discuss suitable designs and quantities.</p>',
      metaTitle: 'Wall Clock Supplier in Delhi | OSIRA',
      metaDescription: 'Wholesale and custom wall clock supplier for Delhi businesses, retailers and projects.',
      nearbyAreas: 'Delhi NCR and nearby business locations.',
      deliveryTime: 'As confirmed for the order',
    },
    {
      cityName: 'Mumbai',
      slug: 'mumbai',
      state: 'Maharashtra',
      pageType: 'supplier',
      h1Heading: 'Wall Clock Supplier in Mumbai for Wholesale & Custom Orders',
      heroSubheading: 'Wall clocks for Mumbai retailers, corporate buyers, hospitality and commercial projects.',
      introContent: '<p>OSIRA supports Mumbai buyers with wall clock options for retail, gifting, promotional and interior requirements.</p>',
      whyChooseContent: '<p>Share the quantity, style and branding brief so the team can recommend a practical product mix.</p>',
      servicesContent: '<p>Wholesale supply, corporate gifting, promotional branding and custom/OEM discussions are available.</p>',
      deliveryContent: '<p>Delivery timelines vary by order size and destination and are confirmed before dispatch.</p>',
      industriesContent: '<p>Useful for stores, offices, hotels, educational institutions, healthcare and residential projects.</p>',
      closingContent: '<p>Tell us what you need and the team will help with the next step.</p>',
      metaTitle: 'Wall Clock Supplier in Mumbai | OSIRA',
      metaDescription: 'Wholesale, custom and business wall clock supplier for Mumbai buyers.',
      nearbyAreas: 'Mumbai and surrounding business locations.',
      deliveryTime: 'As confirmed for the order',
    },
    {
      cityName: 'Ahmedabad',
      slug: 'ahmedabad',
      state: 'Gujarat',
      pageType: 'supplier',
      h1Heading: 'Wall Clock Supplier in Ahmedabad for Business Requirements',
      heroSubheading: 'Source wall clocks for retail, corporate gifting, offices and commercial projects in Ahmedabad.',
      introContent: '<p>OSIRA supplies wall clocks for Ahmedabad businesses that need practical designs, quantity support and custom branding options.</p>',
      whyChooseContent: '<p>Discuss the product type, quantity, target price and branding requirement before placing a business order.</p>',
      servicesContent: '<p>Wholesale, corporate gifting, promotional branding and custom/OEM support are available.</p>',
      deliveryContent: '<p>Delivery is planned around product availability, order size and destination.</p>',
      industriesContent: '<p>Suitable for retail, corporate offices, hospitality, education, healthcare and residential projects.</p>',
      closingContent: '<p>Send your requirement to receive a suitable recommendation.</p>',
      metaTitle: 'Wall Clock Supplier in Ahmedabad | OSIRA',
      metaDescription: 'Wall clock supplier for Ahmedabad retailers, offices, gifting and commercial projects.',
      nearbyAreas: 'Ahmedabad and nearby Gujarat business locations.',
      deliveryTime: 'As confirmed for the order',
    },
  ];

  for (let i = 0; i < cities.length; i++) {
    const city = cities[i];
    await prisma.cityPage.upsert({
      where: { slug: city.slug },
      update: city,
      create: { ...city, displayOrder: i + 1 },
    });
  }

  const posts = [
    {
      title: 'How to Choose Wall Clocks for Different Room Sizes',
      slug: 'how-to-choose-wall-clocks-for-different-room-sizes',
      category: 'Wall Clock Buying Guide',
      description: 'A practical guide to choosing wall clock size, readability and placement for different room dimensions.',
      contentHtml: '<p>The right wall clock should be easy to read from the intended viewing distance while fitting naturally into the room.</p><h2>Start with viewing distance</h2><p>Larger rooms and commercial spaces generally benefit from larger dials or stronger visual contrast.</p><h2>Match the clock to the space</h2><p>Consider the wall width, surrounding furniture, lighting and overall interior direction before choosing a design.</p><h2>For business buyers</h2><p>For multiple rooms or locations, keep the product family consistent where a coordinated look is important.</p>',
      metaTitle: 'How to Choose Wall Clock Size | OSIRA Guide',
      metaDescription: 'Learn how to choose wall clock size, readability and placement for different room sizes.',
    },
    {
      title: 'Wholesale Wall Clocks: What Buyers Should Check Before Ordering',
      slug: 'wholesale-wall-clocks-buyer-checklist',
      category: 'Business Buying',
      description: 'Key points retailers and distributors should confirm before placing a wholesale wall clock order.',
      contentHtml: '<p>Wholesale buying is easier when product, quantity and delivery expectations are clear before the order is confirmed.</p><h2>Check MOQ and pricing</h2><p>Understand minimum quantity and how pricing changes at different order volumes.</p><h2>Check product consistency</h2><p>For repeat orders, confirm the product specification and expected finish so future purchases remain aligned.</p><h2>Confirm packaging and delivery</h2><p>Discuss packaging, dispatch schedule and destination requirements before production or dispatch.</p>',
      metaTitle: 'Wholesale Wall Clock Buyer Checklist | OSIRA',
      metaDescription: 'A practical checklist for retailers and distributors buying wall clocks wholesale.',
    },
    {
      title: 'Custom Wall Clocks for Corporate Gifting and Branding',
      slug: 'custom-wall-clocks-corporate-gifting-branding',
      category: 'Custom & Branding',
      description: 'How businesses can plan branded wall clock programmes for gifting, promotions and milestones.',
      contentHtml: '<p>A branded wall clock can combine useful everyday value with visible business identity.</p><h2>Define the programme</h2><p>Start with event, quantity, audience, budget and delivery date.</p><h2>Plan artwork</h2><p>Confirm logo placement, artwork dimensions and the visual relationship between the brand and the clock design.</p><h2>Allow time for approval</h2><p>For larger programmes, include time for artwork review, sampling where required, production and dispatch.</p>',
      metaTitle: 'Custom Wall Clocks for Corporate Gifting | OSIRA',
      metaDescription: 'Plan custom branded wall clocks for corporate gifting, promotions and business events.',
    },
  ];

  for (const post of posts) {
    await prisma.blog.upsert({
      where: { slug: post.slug },
      update: post,
      create: post,
    });
  }

  const adminEmail = process.env.ADMIN_EMAIL?.trim().toLowerCase();
  const adminPassword = process.env.ADMIN_PASSWORD;
  if (adminEmail && adminPassword && adminPassword !== 'CHANGE_THIS_TO_A_STRONG_PASSWORD') {
    const passwordHash = hashPassword(adminPassword);
    await prisma.adminUser.upsert({
      where: { email: adminEmail },
      update: { passwordHash, isActive: true, name: 'OSIRA Admin' },
      create: { email: adminEmail, passwordHash, name: 'OSIRA Admin', role: 'admin' },
    });
    console.log('OSIRA admin account configured:', adminEmail);
  }

  console.log('OSIRA Prisma seed complete:', rows.length, 'catalogue rows processed');
}

main().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => prisma.$disconnect());
