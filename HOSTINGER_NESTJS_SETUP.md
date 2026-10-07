# OSIRA — NestJS + Prisma + MySQL

## Production stack
- Node.js 22.x
- NestJS 11
- Prisma 6
- MySQL 8 / MariaDB
- EJS server-rendered pages
- GitHub → Hostinger Node.js Web App deployment

## Local development

```bash
npm install
cp .env.example .env
# set DATABASE_URL
npx prisma db push
npm run prisma:seed
npm run start:dev
```

Open `http://localhost:3000`.

## Hostinger deployment

In hPanel:

**Websites → Add Website → Node.js Web App → Import Git Repository**

Recommended:
- Repository: `bhawanirathore7773/omaansh`
- Branch: `main`
- Node.js: **22.x**
- Build command: `npm run build`
- Start command: `npm run start:prod`

Required environment variables:

```env
NODE_ENV=production
PORT=3000
SITE_URL=https://omaansh.com
DATABASE_URL=mysql://USER:PASSWORD@HOST:3306/DATABASE
ADMIN_EMAIL=admin@omaansh.com
ADMIN_PASSWORD=YOUR_STRONG_ADMIN_PASSWORD
```

Do **not** commit `.env`.

### MySQL database

Create the MySQL database/user in Hostinger first. Use the exact Hostinger database hostname, database name, username and password in `DATABASE_URL`.

The database is separate from the Node application files. Prisma connects to it through `DATABASE_URL`.

## Prisma production rule

Development may use:

```bash
npx prisma db push
```

For production, do **not** rely on `db push` as the long-term deployment mechanism. Once the production migration baseline is generated and committed under `prisma/migrations`, Hostinger should run the migration as part of the deployment/build workflow:

```bash
npm run prisma:migrate:deploy
npm run prisma:seed
```

Run `prisma:seed` only after the database schema is present and the seed data has been reviewed. The market-research catalogue is intentionally inserted as inactive draft products.

Use `migrate deploy` for subsequent schema changes as well.

**Important:** do not run `prisma migrate deploy` against the existing Django database until the migration baseline has been reconciled with that database. A baseline must match the actual production schema before Django data is imported.

## Current NestJS routes

Public:
- `/`
- `/products`
- `/products/:slug`
- `/categories`
- `/categories/:slug`
- `/services`
- `/services/:slug`
- `/industries`
- `/industries/:slug`
- `/cities`
- `/cities/:slug`
- `/blog`
- `/blog/:slug`
- `/enquiries`
- `/health`

Admin:
- `/admin/login`
- `/admin`
- `/admin/products`
- `/admin/categories`
- `/admin/enquiries`
- `/admin/services`
- `/admin/industries`
- `/admin/cities`
- `/admin/blog`
- `/admin/settings`

Admin authentication uses a server-side session stored in MySQL and CSRF tokens for state-changing admin actions.

## GitHub Actions

The repository has a NestJS CI workflow that validates Prisma and builds the NestJS application on pushes and pull requests to `main`.

Use the CI result as the first deployment gate.

## Django migration

Django is intentionally still present during migration. Do not delete it yet.

The current Prisma seed creates the new OSIRA content baseline, but it is **not** a complete historical Django database migration. Existing Django enquiries, blogs, cities, industries, services, testimonials, FAQs and any edited product records must be exported and transformed before the old runtime is removed.

Recommended final sequence:

1. Freeze/backup Django production database.
2. Export Django data.
3. Transform/import into the Prisma schema.
4. Verify product URLs, images, SEO metadata and enquiries.
5. Point the domain to the NestJS Hostinger app.
6. Monitor logs and `/health`.
7. Only after successful verification, remove/decommission Django.

## Security checklist

- Strong unique admin password.
- Production `NODE_ENV=production`.
- HTTPS enabled.
- Never commit `.env`.
- Keep admin session cookies secure.
- Keep CSRF protection on admin POST actions.
- Public enquiry and admin-login rate limiting are enabled in the NestJS bootstrap; review the limits before launch.
- Review npm audit findings before final deployment; do not use `npm audit fix --force` blindly.
