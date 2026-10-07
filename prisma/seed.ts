import { PrismaClient } from '@prisma/client';
import { randomBytes, scryptSync } from 'crypto';

const prisma = new PrismaClient();

const slugify = (value: string) =>
  value.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const hashPassword = (password: string) => {
  const salt = randomBytes(16).toString('hex');
  return `scrypt${salt}${scryptSync(password, salt, 64).toString('hex')}`;
};

type ProductSeed = {
  name: string;
  category: string;
  size: string;
  shape: string;
  material: string;
  movement: string;
  finish: string;
  useCase: string;
  description: string;
  price?: number;
  moq?: number;
  featured?: boolean;
  newArrival?: boolean;
};

const categories = [
  ['plastic-wall-clocks','Plastic Wall Clocks','Practical plastic wall clocks for homes, offices, retail counters and institutional spaces.'],
  ['designer-wall-clocks','Designer Wall Clocks','Contemporary wall clock designs for décor stores, modern interiors and premium gifting.'],
  ['decorative-wall-clocks','Decorative Wall Clocks','Decorative wall clocks selected for visual appeal, everyday readability and interior styling.'],
  ['promotional-wall-clocks','Promotional Wall Clocks','Wall clocks for branded campaigns, corporate gifting, dealer programmes and bulk promotions.'],
  ['custom-wall-clocks','Custom Wall Clocks','Custom wall clock programmes for logos, artwork, colour requirements and business orders.'],
  ['corporate-wall-clocks','Corporate Wall Clocks','Business-ready wall clocks for offices, institutions, reception areas and branded spaces.'],
  ['round-wall-clocks','Round Wall Clocks','Classic round wall clocks in practical sizes for everyday spaces and commercial use.'],
  ['square-wall-clocks','Square Wall Clocks','Clean square wall clocks for modern offices, retail interiors and contemporary homes.'],
  ['rectangle-wall-clocks','Rectangle Wall Clocks','Rectangular wall clock formats for distinctive layouts and commercial interiors.'],
  ['large-wall-clocks','Large Wall Clocks','Larger-format wall clocks for halls, reception areas, classrooms and commercial walls.'],
  ['8-inch-wall-clocks','8 Inch Wall Clocks','Compact 8 inch wall clocks for bedrooms, studies, offices, retail displays and smaller spaces.'],
  ['10-inch-wall-clocks','10 Inch Wall Clocks','10 inch wall clocks for compact walls, offices, retail and promotional requirements.'],
  ['12-inch-wall-clocks','12 Inch Wall Clocks','12 inch wall clocks balancing readability, footprint and everyday utility.'],
  ['14-inch-wall-clocks','14 Inch Wall Clocks','14 inch wall clocks for larger walls, offices, halls and commercial spaces.'],
];

const products: ProductSeed[] = [
  {name:'OSIRA Classic Round 10 Inch Wall Clock',category:'plastic-wall-clocks',size:'10 inch',shape:'Round',material:'ABS plastic frame',movement:'Quartz',finish:'Matte',useCase:'Home, office, retail',description:'A clean, easy-to-read round wall clock designed for everyday home, office and retail use.',price:150,moq:25,featured:true},
  {name:'OSIRA Classic Round 12 Inch Wall Clock',category:'plastic-wall-clocks',size:'12 inch',shape:'Round',material:'ABS plastic frame',movement:'Quartz',finish:'Matte',useCase:'Home, office, institutional',description:'A practical 12 inch wall clock with a balanced dial size for clear everyday time reading.',price:199,moq:25,featured:true},
  {name:'OSIRA Classic Round 14 Inch Wall Clock',category:'plastic-wall-clocks',size:'14 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Office, hall, retail',description:'A larger round wall clock for spaces that need stronger visual readability from a distance.',price:300,moq:25},
  {name:'OSIRA Minimal Round 8 Inch Wall Clock',category:'8-inch-wall-clocks',size:'8 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Bedroom, study, office',description:'Compact wall clock for smaller walls, workstations, study areas and retail displays.',moq:25,newArrival:true},
  {name:'OSIRA Minimal Round 10 Inch Wall Clock',category:'10-inch-wall-clocks',size:'10 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Home, office, retail',description:'A compact everyday wall clock with a simple dial and practical footprint.',price:150,moq:25},
  {name:'OSIRA Clear Dial 12 Inch Wall Clock',category:'12-inch-wall-clocks',size:'12 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Gloss',useCase:'Office, classroom, home',description:'A readable 12 inch wall clock for spaces where quick time visibility matters.',price:199,moq:25,featured:true},
  {name:'OSIRA Modern Square 10 Inch Wall Clock',category:'square-wall-clocks',size:'10 inch',shape:'Square',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Office, retail, home',description:'A square wall clock with a structured silhouette for modern interiors.',price:110,moq:25,featured:true},
  {name:'OSIRA Modern Square 12 Inch Wall Clock',category:'square-wall-clocks',size:'12 inch',shape:'Square',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Office, reception, home',description:'A practical square format with a larger dial for improved wall presence.',moq:25},
  {name:'OSIRA Rectangle Office Wall Clock',category:'rectangle-wall-clocks',size:'12 inch class',shape:'Rectangle',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Office, reception, commercial',description:'A rectangular wall clock concept for contemporary office and commercial interiors.',moq:25,newArrival:true},
  {name:'OSIRA Designer Line Wall Clock',category:'designer-wall-clocks',size:'12 inch class',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Decorative',useCase:'Home, décor store, gifting',description:'A decorative wall clock direction for buyers looking for a stronger visual element than a basic timepiece.',moq:25,featured:true},
  {name:'OSIRA Decorative Floral Wall Clock',category:'decorative-wall-clocks',size:'12 inch class',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Decorative',useCase:'Home, boutique, gifting',description:'A decorative wall clock style intended to complement colourful and traditional interiors.',moq:25},
  {name:'OSIRA Decorative Contemporary Wall Clock',category:'decorative-wall-clocks',size:'14 inch class',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Decorative',useCase:'Living room, office, hospitality',description:'A larger decorative format for walls that need both time visibility and visual character.',moq:25},
  {name:'OSIRA Corporate Logo Wall Clock',category:'promotional-wall-clocks',size:'10-12 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Custom artwork',useCase:'Corporate gifting, promotions',description:'A promotional wall clock format that can be discussed for business branding, artwork and quantity requirements.',moq:100,featured:true},
  {name:'OSIRA Promotional Business Wall Clock',category:'promotional-wall-clocks',size:'10 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Custom artwork',useCase:'Dealer gifts, campaigns',description:'A business-order wall clock concept for promotional campaigns and quantity-led gifting.',moq:100},
  {name:'OSIRA Custom Brand Wall Clock',category:'custom-wall-clocks',size:'10-14 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Custom',useCase:'Branding, gifting, institutional',description:'A custom programme for customers who need a logo, artwork, colour or design discussion before production.',moq:100,featured:true},
  {name:'OSIRA Custom Logo Square Clock',category:'custom-wall-clocks',size:'10-12 inch',shape:'Square',material:'Plastic frame',movement:'Quartz',finish:'Custom',useCase:'Corporate, retail, events',description:'A square custom wall clock option for branded business programmes and institutional orders.',moq:100},
  {name:'OSIRA Corporate Office Wall Clock',category:'corporate-wall-clocks',size:'12 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Office, reception, meeting room',description:'An understated wall clock format for workplaces, reception areas and meeting spaces.',moq:25},
  {name:'OSIRA Reception Wall Clock 14 Inch',category:'corporate-wall-clocks',size:'14 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Reception, institution, office',description:'A larger-format office clock designed for visibility across reception and common areas.',moq:25,featured:true},
  {name:'OSIRA Round Everyday Clock 8 Inch',category:'round-wall-clocks',size:'8 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Bedroom, study, retail',description:'A compact round clock for smaller spaces and display applications.',moq:25},
  {name:'OSIRA Round Everyday Clock 10 Inch',category:'round-wall-clocks',size:'10 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Home, office, retail',description:'An everyday round clock format suited to common residential and commercial spaces.',moq:25},
  {name:'OSIRA Round Everyday Clock 12 Inch',category:'round-wall-clocks',size:'12 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Home, office, institution',description:'A versatile 12 inch round wall clock for clear everyday time reading.',moq:25},
  {name:'OSIRA Large Visibility 14 Inch Clock',category:'large-wall-clocks',size:'14 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Hall, office, classroom',description:'A larger wall clock for spaces where the dial needs to remain visible from farther away.',price:300,moq:25},
  {name:'OSIRA Large Visibility 16 Inch Clock',category:'large-wall-clocks',size:'16 inch class',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Hall, reception, commercial',description:'A larger wall clock format for commercial spaces with broader viewing distances.',moq:25},
  {name:'OSIRA 14 Inch Decorative Clock',category:'14-inch-wall-clocks',size:'14 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Decorative',useCase:'Home, office, hospitality',description:'A 14 inch decorative wall clock format for larger interior walls.',price:300,moq:25},
  {name:'OSIRA 12 Inch Promotional Clock',category:'promotional-wall-clocks',size:'12 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Custom artwork',useCase:'Corporate campaigns',description:'A 12 inch promotional format for branded business requirements subject to artwork and quantity confirmation.',moq:100},
  {name:'OSIRA Square Business Clock',category:'square-wall-clocks',size:'10 inch',shape:'Square',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Office, retail, promotion',description:'A square business-oriented wall clock format for clean modern displays.',moq:25},
  {name:'OSIRA 10 Inch Custom Promotional Clock',category:'10-inch-wall-clocks',size:'10 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Custom artwork',useCase:'Promotional, gifting',description:'A 10 inch format for promotional orders where branding and quantity are part of the buying brief.',moq:100},
  {name:'OSIRA 12 Inch Custom Brand Clock',category:'12-inch-wall-clocks',size:'12 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Custom artwork',useCase:'Corporate, dealer, institutional',description:'A 12 inch custom wall clock format for business branding and gifting requirements.',moq:100},
  {name:'OSIRA Rectangle Business Clock',category:'rectangle-wall-clocks',size:'10-12 inch class',shape:'Rectangle',material:'Plastic frame',movement:'Quartz',finish:'Matte',useCase:'Office, retail, commercial',description:'A clean rectangular format for business and contemporary interior applications.',moq:25},
  {name:'OSIRA Decorative Retail Display Clock',category:'decorative-wall-clocks',size:'10-12 inch',shape:'Round',material:'Plastic frame',movement:'Quartz',finish:'Decorative',useCase:'Retail, gifting, décor',description:'A decorative format for retail shelves, décor displays and everyday gifting programmes.',moq:25},
];

async function main() {
  console.log('OSIRA fresh database seed: clearing application data...');

  await prisma.bannerProduct.deleteMany();
  await prisma.industryProduct.deleteMany();
  await prisma.adminSession.deleteMany();
  await prisma.enquiry.deleteMany();
  await prisma.product.deleteMany();
  await prisma.category.deleteMany();
  await prisma.pricingTierTemplate.deleteMany();
  await prisma.fAQ.deleteMany();
  await prisma.testimonial.deleteMany();
  await prisma.banner.deleteMany();
  await prisma.servicePage.deleteMany();
  await prisma.industryPage.deleteMany();
  await prisma.cityPage.deleteMany();
  await prisma.blog.deleteMany();
  await prisma.adminUser.deleteMany();

  await prisma.siteSettings.upsert({
    where: { id: 1 },
    update: {
      businessName: 'OSIRA',
      tagline: 'Wall clocks for homes, workplaces, retailers and business orders',
      defaultMetaTitle: 'Wall Clock Manufacturer in Jaipur | OSIRA',
      defaultMetaDescription: 'OSIRA supplies wall clocks from Jaipur for retail, wholesale, corporate gifting, promotional branding and custom business requirements.',
    },
    create: {
      id: 1,
      businessName: 'OSIRA',
      tagline: 'Wall clocks for homes, workplaces, retailers and business orders',
      gstNumber: '08BVNPS9491J1ZG',
      defaultMetaTitle: 'Wall Clock Manufacturer in Jaipur | OSIRA',
      defaultMetaDescription: 'OSIRA supplies wall clocks from Jaipur for retail, wholesale, corporate gifting, promotional branding and custom business requirements.',
    },
  });

  const categoryMap = new Map<string, number>();
  for (let i = 0; i < categories.length; i++) {
    const [slug, name, description] = categories[i];
    const category = await prisma.category.create({
      data: {
        slug, name, description,
        h1Heading: name,
        metaTitle: `${name} | OSIRA Jaipur`.slice(0, 70),
        metaDescription: `${description} Request wholesale and business pricing from OSIRA.`.slice(0, 160),
        seoContent: `<p>${description}</p><p>OSIRA supports product selection, quantity planning and business enquiries. Specifications, availability, pricing and customisation should be confirmed for the current requirement.</p>`,
        displayOrder: i + 1,
        isFeatured: i < 8,
      },
    });
    categoryMap.set(slug, category.id);
  }

  for (let i = 0; i < products.length; i++) {
    const p = products[i];
    const categoryId = categoryMap.get(p.category);
    if (!categoryId) throw new Error(`Missing category: ${p.category}`);
    const slug = slugify(p.name);
    await prisma.product.create({
      data: {
        name: p.name,
        slug,
        categoryId,
        description: p.description,
        shortDescription: `${p.size} ${p.shape.toLowerCase()} wall clock for ${p.useCase.toLowerCase()}.`,
        specifications: [`Size: ${p.size}`, `Shape: ${p.shape}`, `Material: ${p.material}`, `Movement: ${p.movement}`, `Finish: ${p.finish}`, `Application: ${p.useCase}`, `MOQ: ${p.moq || 1} units`].join('\\n'),
        price: p.price ?? null,
        moq: p.moq || 1,
        metaTitle: `${p.name} | OSIRA`.slice(0, 70),
        metaDescription: `${p.description} View specifications and enquire for current OSIRA pricing and availability.`.slice(0, 160),
        metaKeywords: [`${p.size} wall clock`, `${p.shape.toLowerCase()} wall clock`, 'wall clock supplier Jaipur'].join(', '),
        brand: 'OSIRA',
        sku: `OS-${String(i + 1).padStart(4, '0')}`,
        availability: 'InStock',
        isFeatured: !!p.featured,
        isNewArrival: !!p.newArrival,
        isActive: true,
      },
    });
  }

  await prisma.pricingTierTemplate.create({
    data: { name: 'Business Default', description: 'Quantity-led pricing framework. Final quote depends on product, artwork, packaging and delivery.' },
  });

  const services = [
    ['Wholesale Wall Clocks','wholesale-wall-clocks','Wholesale wall clocks for retailers, dealers and distributors','Source wall clocks for retail and distribution requirements with quantity-led commercial discussions.'],
    ['Corporate Gifting','corporate-gifting','Corporate gifting wall clocks with business branding','Wall clocks for employee gifts, dealer programmes, anniversaries, milestones and institutional gifting.'],
    ['Promotional Branding','promotional-wall-clocks','Promotional wall clocks for branded campaigns','Plan branded wall clock orders around logo artwork, quantity, packaging and delivery requirements.'],
    ['Custom & OEM','custom-oem-wall-clocks','Custom and OEM wall clock programmes','Discuss product format, dimensions, artwork, colours and business quantities for a custom programme.'],
  ];
  for (let i=0;i<services.length;i++) {
    const [name,slug,h1,desc]=services[i];
    await prisma.servicePage.create({data:{
      name,slug,h1Heading:h1,heroSubheading:desc,shortDescription:desc,
      fullDescription:`<p>${desc}</p><p>Share the required quantity, product direction, branding or packaging brief. OSIRA can confirm feasibility, current pricing and delivery details for the specific requirement.</p>`,
      processContent:'<ol><li>Share quantity and product requirement.</li><li>Review suitable designs and specifications.</li><li>Confirm artwork, pricing and commercial terms.</li><li>Approve production and dispatch plan.</li></ol>',
      benefitsContent:'<p>Clear requirement-based communication, product selection support and quantity-focused ordering.</p>',
      metaTitle:`${h1} | OSIRA`.slice(0,70),metaDescription:desc.slice(0,160),displayOrder:i+1
    }});
  }

  const industries = [
    ['Retail Stores','retail-stores','Wall clocks for retail stores and dealers'],
    ['Corporate Offices','corporate-offices','Wall clocks for offices, reception areas and workplaces'],
    ['Hotels & Hospitality','hotels-hospitality','Wall clocks for hospitality interiors and common areas'],
    ['Schools & Institutions','schools-institutions','Wall clocks for classrooms, institutions and administrative spaces'],
    ['Corporate Gifting','corporate-gifting-industry','Wall clocks for employee, dealer and milestone gifting'],
    ['Advertising & Promotions','advertising-promotions','Promotional wall clocks for branded campaigns'],
  ];
  for (let i=0;i<industries.length;i++) {
    const [name,slug,h1]=industries[i];
    await prisma.industryPage.create({data:{
      industryName:name,slug,h1Heading:h1,heroSubheading:'Choose a suitable wall clock format for your space or business programme.',
      introContent:`<p>OSIRA supports ${name.toLowerCase()} with wall clock options covering practical, decorative and business-order requirements.</p>`,
      benefitsContent:'<p>Product selection can be aligned to size, shape, readability, branding, quantity and delivery requirements.</p>',
      customizationContent:'<p>For business programmes, share artwork, quantity and desired format so current options can be reviewed.</p>',
      metaTitle:`${h1} | OSIRA`.slice(0,70),metaDescription:`Wall clocks for ${name.toLowerCase()} from OSIRA. Explore suitable formats and enquire for current business pricing.`.slice(0,160),
      displayOrder:i+1
    }});
  }

  const cities = [
    {
      cityName:'Jaipur',slug:'jaipur',state:'Rajasthan',h1:'Wall Clock Manufacturer in Jaipur',
      intro:'<p>OSIRA is presented as a Jaipur-based wall clock business serving retail, wholesale, corporate gifting, promotional branding and custom order enquiries. Buyers can browse the catalogue first and then share quantity, size, application and delivery requirements.</p><p>For Jaipur buyers, the useful starting point is the product format and order requirement rather than a generic catalogue promise. Current price, availability, branding feasibility and dispatch details should be confirmed before an order is approved.</p>',
      why:'<p>OSIRA keeps the buying journey focused on product selection and requirement-based quotation. Retailers can compare practical formats, while organisations can discuss branded or quantity-led orders.</p>',
      services:'<p>Wholesale supply, corporate gifting, promotional wall clocks and custom/OEM discussions are available through the business enquiry process.</p>',
      delivery:'<p>For Jaipur orders, delivery or pickup arrangements depend on product availability, quantity and the agreed commercial terms. Do not rely on a fixed delivery promise until the current order is confirmed.</p>',
      areas:'Jaipur business and commercial areas including Gokulpura, Kalwar Road, Vaishali Nagar, Jhotwara, Sikar Road, Mansarovar and Sitapura.',
      industries:'<p>Relevant buyers include retailers, offices, institutions, hospitality businesses, corporate gifting teams and promotional agencies.</p>',
      close:'<p>Share the product or collection, approximate quantity and delivery requirement to request a current quotation.</p>'
    },
    {
      cityName:'Delhi',slug:'delhi',state:'Delhi',h1:'Wall Clock Supplier for Delhi Buyers',
      intro:'<p>OSIRA accepts enquiries for wall clocks required by Delhi retailers, offices, institutions, gifting teams and promotional buyers. The catalogue provides a starting point for comparing sizes, shapes and business-use formats.</p><p>Delhi orders can be discussed around quantity, product selection, branding and delivery requirements. Commercial terms are confirmed for the specific order.</p>',
      why:'<p>A requirement-led process helps Delhi buyers compare suitable wall clock formats without assuming that one product or price fits every order.</p>',
      services:'<p>Wholesale, corporate gifting, promotional branding and custom wall clock requirements can be discussed.</p>',
      delivery:'<p>Delivery timing depends on destination, quantity, stock or production requirements and the confirmed order terms.</p>',
      areas:'Business and commercial locations across Delhi; provide the exact delivery area with the enquiry.',
      industries:'<p>Retail, corporate offices, institutions, hospitality and promotional programmes are common business-use contexts for wall clocks.</p>',
      close:'<p>Send the quantity, preferred format and delivery area to begin a Delhi business enquiry.</p>'
    },
    {
      cityName:'Gurugram',slug:'gurugram',state:'Haryana',h1:'Wall Clock Supplier for Gurugram Buyers',
      intro:'<p>OSIRA supports Gurugram enquiries for office wall clocks, retail supply, corporate gifting and promotional requirements. Buyers can use the catalogue to shortlist practical and business-oriented formats.</p><p>For larger requirements, share the intended application, quantity, branding and delivery details so the current commercial option can be confirmed.</p>',
      why:'<p>Gurugram workplaces and business programmes can require different clock sizes and visual styles. The enquiry process keeps the selection tied to the actual application.</p>',
      services:'<p>Wholesale, corporate gifting, promotional branding and custom/OEM discussions are available.</p>',
      delivery:'<p>Delivery is confirmed according to product, order quantity, destination and production or dispatch requirements.</p>',
      areas:'Commercial and business areas across Gurugram; include the delivery location in your enquiry.',
      industries:'<p>Corporate offices, retail, hospitality, institutions and promotional programmes can use the available wall clock ranges.</p>',
      close:'<p>Tell us the application, quantity and preferred size to request suitable options for Gurugram.</p>'
    },
    {
      cityName:'Noida',slug:'noida',state:'Uttar Pradesh',h1:'Wall Clock Supplier for Noida Buyers',
      intro:'<p>OSIRA provides a catalogue and enquiry route for Noida buyers looking for wall clocks for offices, retail stores, institutions, gifting or promotional programmes.</p><p>Business buyers can shortlist a product and then confirm quantity, specifications, branding requirements and delivery terms for the order.</p>',
      why:'<p>The catalogue separates everyday wall clocks from promotional and custom requirements, making it easier to start with the intended application.</p>',
      services:'<p>Wholesale, corporate gifting, promotional branding and custom/OEM wall clock enquiries are supported.</p>',
      delivery:'<p>Delivery timing is requirement-specific and depends on the destination, quantity, product availability and agreed terms.</p>',
      areas:'Commercial and business areas across Noida; provide the specific delivery location when enquiring.',
      industries:'<p>Office, retail, education, hospitality and corporate programmes can be relevant applications.</p>',
      close:'<p>Send your quantity, preferred format and delivery location to start a Noida enquiry.</p>'
    },
    {
      cityName:'Ahmedabad',slug:'ahmedabad',state:'Gujarat',h1:'Wall Clock Supplier for Ahmedabad Buyers',
      intro:'<p>OSIRA accepts Ahmedabad enquiries for wall clocks used in retail, corporate spaces, institutions, gifting and promotional campaigns. Product pages provide the initial specifications and business-order context.</p><p>For quantity orders, current pricing and availability should be confirmed against the exact product, quantity, branding and delivery requirement.</p>',
      why:'<p>A product-first catalogue helps Ahmedabad buyers compare wall clock formats before moving to a requirement-specific commercial discussion.</p>',
      services:'<p>Wholesale, corporate gifting, promotional branding and custom/OEM programmes can be discussed.</p>',
      delivery:'<p>Delivery depends on destination, quantity, product availability and confirmed dispatch terms.</p>',
      areas:'Commercial and business areas across Ahmedabad; include the delivery location in the enquiry.',
      industries:'<p>Retailers, offices, institutions, hospitality businesses and promotional buyers can explore relevant formats.</p>',
      close:'<p>Share the product direction, quantity and delivery details to request an Ahmedabad quotation.</p>'
    },
    {
      cityName:'Mumbai',slug:'mumbai',state:'Maharashtra',h1:'Wall Clock Supplier for Mumbai Buyers',
      intro:'<p>OSIRA supports Mumbai business enquiries for wall clocks across retail, corporate gifting, promotional branding and commercial interiors. The catalogue can be used to shortlist suitable products before requesting a quote.</p><p>For business orders, quantity, specification, branding, packaging and destination can influence the final commercial terms.</p>',
      why:'<p>Mumbai buyers can start with the required application and clock format, then confirm the current availability and commercial option for the order.</p>',
      services:'<p>Wholesale, corporate gifting, promotional branding and custom/OEM wall clock enquiries are supported.</p>',
      delivery:'<p>Delivery timing is confirmed for the individual order based on product, quantity, destination and dispatch requirements.</p>',
      areas:'Commercial and business locations across Mumbai; provide the delivery area when submitting an enquiry.',
      industries:'<p>Retail, offices, hospitality, institutions, gifting teams and promotional agencies are relevant use cases.</p>',
      close:'<p>Share the quantity, preferred product style and delivery location to begin a Mumbai enquiry.</p>'
    }
  ];
  for (let i=0;i<cities.length;i++) {
    const c=cities[i];
    await prisma.cityPage.create({data:{
      cityName:c.cityName,slug:c.slug,state:c.state,pageType:'supplier',h1Heading:c.h1,heroSubheading:'Business-ready wall clocks with requirement-based enquiry support.',
      introContent:c.intro,whyChooseContent:c.why,servicesContent:c.services,deliveryContent:c.delivery,
      industriesContent:c.industries,closingContent:c.close,metaTitle:(c.h1+' | OSIRA').slice(0,70),
      metaDescription:(c.h1+'. Explore wholesale, corporate gifting and custom wall clock enquiries from OSIRA.').slice(0,160),
      nearbyAreas:c.areas,displayOrder:i+1
    }});
  }

  const blogs = [
    ['How to Choose a Wall Clock for an Office','how-to-choose-a-wall-clock-for-an-office','Office wall clock buying guide','Compare clock size, readability, wall distance, room use and visual style before selecting an office wall clock.'],
    ['Wall Clock Sizes Explained: 8, 10, 12 and 14 Inch','wall-clock-sizes-8-10-12-14-inch','Wall clock size guide','Understand how 8, 10, 12 and 14 inch wall clocks differ in footprint and typical applications.'],
    ['Promotional Wall Clocks for Corporate Branding','promotional-wall-clocks-corporate-branding','Promotional wall clock guide','A practical guide to logo placement, quantities, artwork, packaging and planning branded wall clock orders.'],
    ['Plastic Wall Clocks: Practical Buying Guide','plastic-wall-clocks-buying-guide','Plastic wall clock buying guide','Learn what to check when buying plastic wall clocks for homes, offices, retail and institutional applications.'],
    ['Wholesale Wall Clock Buying Guide for Retailers','wholesale-wall-clock-buying-guide','Wholesale wall clock guide','Plan a wholesale wall clock purchase around product mix, MOQ, pricing, packaging and repeat demand.'],
  ];
  for (const [title,slug,category,desc] of blogs) {
    await prisma.blog.create({data:{
      title,slug,category,description:desc,
      contentHtml:`<p>${desc}</p><h2>What to compare</h2><p>Compare size, shape, material, movement, finish, application, quantity and current commercial terms. Product availability and pricing can change, so confirm the current specification before ordering.</p><h2>For business buyers</h2><p>Share quantity, preferred designs, branding requirements and delivery city to receive a requirement-specific response.</p>`,
      metaTitle:`${title} | OSIRA`.slice(0,70),metaDescription:desc.slice(0,160),isPublished:true
    }});
  }

  const faqs = [
    ['Do you supply wall clocks in bulk?','Yes. OSIRA accepts business enquiries for wholesale, promotional, corporate gifting and custom requirements. Quantity and product-specific terms should be confirmed for the current order.'],
    ['Can I request a custom logo wall clock?','Yes. Share the logo or artwork, preferred clock format and quantity. Feasibility, artwork requirements, MOQ and pricing can then be confirmed.'],
    ['What wall clock sizes are available?','The catalogue covers compact and larger formats including 8, 10, 12 and 14 inch classes, plus selected larger business formats.'],
    ['How do I get the latest price?','Use the enquiry form with the product name and quantity. Product prices can vary by quantity, customization, packaging and delivery requirements.'],
    ['Do you supply outside Jaipur?','Business enquiries can be submitted with the delivery city. Delivery feasibility and timeline depend on the order and destination.'],
  ];
  for (let i=0;i<faqs.length;i++) await prisma.fAQ.create({data:{question:faqs[i][0],answer:faqs[i][1],displayOrder:i+1,scope:'global'}});

  const adminEmail=process.env.ADMIN_EMAIL;
  const adminPassword=process.env.ADMIN_PASSWORD;
  if (adminEmail && adminPassword && adminPassword !== 'CHANGE_THIS_TO_A_STRONG_PASSWORD') {
    await prisma.adminUser.create({data:{email:adminEmail.toLowerCase(),name:'OSIRA Admin',passwordHash:hashPassword(adminPassword),role:'admin'}});
    console.log('Admin user created from ADMIN_EMAIL / ADMIN_PASSWORD.');
  } else {
    console.log('No production admin created. Set ADMIN_EMAIL and ADMIN_PASSWORD before running the seed.');
  }

  console.log(`Fresh OSIRA seed complete: ${categories.length} categories, ${products.length} products, ${services.length} services, ${industries.length} industries, ${cities.length} city pages, ${blogs.length} guides.`);
}

main().catch(async (error) => {
  console.error(error);
  process.exitCode = 1;
}).finally(async () => {
  await prisma.$disconnect();
});
