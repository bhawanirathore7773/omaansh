# SEO release checklist — OSIRA

## Code and configuration

- [x] Set example `SITE_URL` to `https://www.omaansh.com`.
- [x] Use the same www origin as the fallback for controller canonical URLs and schema URLs.
- [x] Keep `robots.txt` Sitemap directive absolute when the site origin is configured.
- [x] Make sitemap URLs absolute and omit reseller URLs/materials unless the reseller programme is published.
- [x] Add homepage Organization, LocalBusiness and WebSite JSON-LD with OSIRA as brand and Omaansh Industries as legal name.
- [x] Align homepage H1 with the primary Jaipur manufacturer query.
- [x] Differentiate Jaipur city-page title/H1 from homepage intent.
- [x] Remove unsupported team-count claim and remove visible photo-upload placeholder prompts from About.
- [ ] Set production Hostinger environment variable `SITE_URL=https://www.omaansh.com` and restart/redeploy the app.
- [ ] Verify the live site serves HTTPS, and HTTP/non-www redirects to the selected canonical host.
- [ ] Confirm canonical tags on homepage, products, categories, services, city pages, blogs and About.
- [ ] Fetch `/robots.txt` and `/sitemap.xml` from production; check for absolute URLs, valid XML and only indexable/published pages.
- [ ] Confirm the homepage canonical is exactly `https://www.omaansh.com/` (or the site's chosen slash convention, consistently).
- [ ] Run Schema Markup Validator / Rich Results Test against the deployed homepage and fix validation errors.
- [ ] Run a production build and smoke-test the home page, product/category pages, enquiries, admin login and sitemap before merging.
- [ ] Do not run `prisma:seed`, `prisma:fresh`, database reset or destructive migrations on production.
- [ ] Verify Hostinger deployment source/branch before release; GitHub commits alone do not update production.

## Content and indexation

- [ ] Review live database/admin meta titles and descriptions; existing SiteSettings can override template defaults.
- [ ] Check category pages for active products and unique useful content before indexing.
- [ ] Review all published city and industry pages for doorway/thin-content risk.
- [ ] Check filtered catalogue URLs and pagination for duplicate/crawl-trap behaviour.
- [ ] Verify no demo/testimonial content, placeholder images, unsupported employee count, unverified certifications, client logos or unconfirmed claims are public.
- [ ] Confirm current MOQ, facility/capacity statements, operating hours and contact details before displaying them as facts.
- [ ] Add real alt text to actual product/factory photos; do not describe stock images as OSIRA's facility.
- [ ] Confirm all important pages have internal links and no orphan pages.

## Google Search Console and measurement

- [ ] Verify the Domain property for `omaansh.com` in Google Search Console.
- [ ] Submit `https://www.omaansh.com/sitemap.xml`.
- [ ] Inspect homepage, Jaipur page, wholesale, corporate gifting and custom/OEM URLs.
- [ ] Track impressions, clicks, CTR, average position and enquiries by landing page/query.
- [ ] Record baseline before release and review after 2, 4 and 8 weeks; rankings are not guaranteed.
- [ ] Check Core Web Vitals using PageSpeed Insights / CrUX after the live site is reachable.

## Rollback

- Revert the SEO branch/commit if templates fail to render or core enquiry/admin functionality breaks.
- Restore only code/configuration; never restore database from seed data.
- Keep production DB and uploaded media untouched during SEO rollout.
