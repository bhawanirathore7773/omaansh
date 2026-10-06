# OSIRA — NestJS + Prisma + MySQL

The Django application is being migrated to a Node.js backend without changing the public brand direction.

## Stack
- Node.js 22+
- NestJS 11
- Prisma 6
- MySQL 8 / MariaDB
- EJS for server-rendered pages
- Existing `static/` assets are served at `/static/`

## Local setup

```bash
npm install
cp .env.example .env
# edit DATABASE_URL
npx prisma db push
npm run prisma:seed
npm run start:dev
```

Open `http://localhost:3000`.

## Hostinger

Hostinger supports NestJS Node.js Web Apps on Business and Cloud hosting. Connect this GitHub repository through:

**hPanel → Websites → Add Website → Node.js Web App → Import Git Repository**

Recommended settings:

- Framework: NestJS
- Node.js: 22.x
- Build command: `npm run build`
- Start command: `npm run start`
- Entry/output: use the detected NestJS defaults
- Environment variable:
  - `NODE_ENV=production`
  - `DATABASE_URL=mysql://USER:PASSWORD@HOST:3306/DATABASE`

Create the MySQL database in Hostinger first, then copy its credentials into `DATABASE_URL`.

After the first deployment, run Prisma schema setup from the Hostinger terminal if available:

```bash
npx prisma db push
npm run prisma:seed
```

Do not commit `.env`.

## Current migration state

The repository now contains a NestJS/Prisma foundation alongside the existing Django code so the public website does not have to be taken offline during migration.

The first Node pages are:
- `/`
- `/products`
- `/products/:slug`
- `/api/products`
- `/api/products/:slug`
- `/health`

The Prisma schema covers the main Django content model: products, categories, pricing tiers, city pages, industry pages, services, banners, FAQs, testimonials, blogs, site settings and enquiries.

The repository CSV catalogue can be seeded into MySQL with `npm run prisma:seed`.

The next migration phase should move the remaining public Django pages and enquiry/admin workflows to NestJS before the Django runtime is removed.
