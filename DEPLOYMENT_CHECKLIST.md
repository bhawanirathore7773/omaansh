# HOOVALE Django Project - Deployment Checklist

## Pre-Deployment (Development Phase)

### Local Setup
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install all dependencies from requirements.txt
- [ ] Copy .env.example to .env
- [ ] Configure local settings in .env
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Test runserver locally: `python manage.py runserver`
- [ ] Access http://localhost:8000
- [ ] Access admin at http://localhost:8000/admin

### Testing
- [ ] Test home page loads correctly
- [ ] Test product listing with filters
- [ ] Test product detail page
- [ ] Test search functionality
- [ ] Test enquiry form submission
- [ ] Test WhatsApp integration
- [ ] Test responsive design (mobile, tablet, desktop)
- [ ] Test form validation
- [ ] Test 404 and 500 error pages
- [ ] Test sitemap.xml generation

### Content Setup
- [ ] Add at least one product category
- [ ] Add sample products (5-10)
- [ ] Upload product images
- [ ] Set up product metadata (SEO fields)
- [ ] Configure Open Graph tags
- [ ] Update contact information in footer
- [ ] Update WhatsApp number
- [ ] Update company details

## Pre-Deployment (Security & Configuration)

### Django Settings
- [ ] Generate strong SECRET_KEY for production
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS with actual domain
- [ ] Set secure cookie settings
- [ ] Configure CSRF trusted origins
- [ ] Enable HTTPS redirect (SECURE_SSL_REDIRECT = True)
- [ ] Set HSTS security headers
- [ ] Configure email backend for production
- [ ] Set up proper logging configuration

### Database
- [ ] Choose PostgreSQL for production (not SQLite)
- [ ] Create production database
- [ ] Create database user with strong password
- [ ] Test database connection
- [ ] Take backup of development database
- [ ] Document database credentials securely

### Static Files & Media
- [ ] Configure static files storage
- [ ] Configure media files location
- [ ] Set proper permissions (755 for folders, 644 for files)
- [ ] Consider using CDN for static files
- [ ] Configure CloudFlare or similar CDN
- [ ] Test static files loading

### Email Configuration
- [ ] Configure email backend
- [ ] Set up SMTP credentials
- [ ] Test email sending
- [ ] Create email templates for enquiries
- [ ] Configure admin email

### SEO & Analytics
- [ ] Create sitemap.xml
- [ ] Create robots.txt
- [ ] Add Google Analytics tracking code
- [ ] Submit sitemap to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Configure Open Graph tags for social sharing
- [ ] Test social media sharing

### Security Measures
- [ ] Install and configure SSL certificate
- [ ] Enable HTTPS
- [ ] Configure security headers
- [ ] Set up firewall rules
- [ ] Configure rate limiting
- [ ] Enable CSRF protection
- [ ] Implement XSS protection
- [ ] Set up intrusion detection

## Deployment

### PythonAnywhere Deployment

#### Account & Setup
- [ ] Create PythonAnywhere account
- [ ] Upload project code
- [ ] Create web app with Python 3.9+

#### Configuration
- [ ] Set WSGI file path to `pythonanywhere_wsgi.py`
- [ ] Configure virtualenv path
- [ ] Set working directory

#### Environment Variables
- [ ] Configure SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Set ALLOWED_HOSTS
- [ ] Configure database URL (if PostgreSQL)
- [ ] Set email configuration
- [ ] Configure other environment variables

#### Database
- [ ] Set up PostgreSQL (or use SQLite)
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Collect static files

#### Web App
- [ ] Reload web app
- [ ] Check for error logs
- [ ] Test website functionality
- [ ] Verify HTTPS is working

### Render.com Deployment

#### GitHub Setup
- [ ] Push code to GitHub
- [ ] Ensure .env is in .gitignore

#### Render Configuration
- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Create new Web Service
- [ ] Set build and start commands

#### Environment Variables
- [ ] Set DEBUG=False
- [ ] Set SECRET_KEY
- [ ] Set ALLOWED_HOSTS with Render domain
- [ ] Configure DATABASE_URL
- [ ] Configure email settings
- [ ] Configure other variables

#### Deployment
- [ ] Deploy from render.yaml
- [ ] Watch build logs for errors
- [ ] Test deployed website
- [ ] Configure custom domain (if applicable)

### VPS Deployment (Ubuntu/Debian)

#### Server Setup
- [ ] SSH into server
- [ ] Update system: `sudo apt update && sudo apt upgrade`
- [ ] Install Python, PostgreSQL, Nginx

#### Project Setup
- [ ] Clone repository to /var/www
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Create and configure .env file

#### Database Setup
- [ ] Create PostgreSQL database
- [ ] Create database user
- [ ] Grant privileges
- [ ] Update Django settings with database config
- [ ] Run migrations

#### Application Setup
- [ ] Collect static files
- [ ] Create systemd service file
- [ ] Set proper permissions
- [ ] Enable and start service

#### Web Server Setup
- [ ] Configure Nginx virtual host
- [ ] Configure SSL certificate (Let's Encrypt)
- [ ] Enable Nginx sites
- [ ] Test Nginx configuration
- [ ] Restart Nginx

#### Testing
- [ ] Test website access
- [ ] Test admin panel
- [ ] Verify SSL certificate
- [ ] Check logs for errors
- [ ] Test all functionality

## Post-Deployment

### Verification
- [ ] Test website on desktop
- [ ] Test website on mobile/tablet
- [ ] Test all pages load correctly
- [ ] Test enquiry form submission
- [ ] Test WhatsApp integration
- [ ] Test search and filters
- [ ] Test admin panel access
- [ ] Verify SSL certificate validity

### Monitoring & Logging
- [ ] Set up log rotation
- [ ] Monitor application logs
- [ ] Set up error email notifications
- [ ] Monitor server resources (CPU, RAM, disk)
- [ ] Set up uptime monitoring
- [ ] Configure backup alerts

### Backups
- [ ] Set up automatic database backups
- [ ] Set up media files backup
- [ ] Configure backup retention policy
- [ ] Test backup restoration
- [ ] Document backup procedures

### Domain & DNS
- [ ] Configure domain DNS records
- [ ] Update nameservers (if applicable)
- [ ] Verify DNS propagation
- [ ] Configure MX records for email
- [ ] Test email functionality

### SEO Post-Launch
- [ ] Submit sitemap to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Create Google Business Profile
- [ ] Submit to business directories
- [ ] Monitor search rankings
- [ ] Set up Google Analytics

### Performance Optimization
- [ ] Enable caching (browser, server)
- [ ] Configure CDN for static files
- [ ] Optimize images
- [ ] Minify CSS/JavaScript
- [ ] Enable gzip compression
- [ ] Test page load speed

### Maintenance Schedule

#### Daily
- [ ] Monitor application logs
- [ ] Check server health
- [ ] Review new enquiries

#### Weekly
- [ ] Backup database and media
- [ ] Review and respond to enquiries
- [ ] Check website uptime
- [ ] Monitor server resources

#### Monthly
- [ ] Update dependencies
- [ ] Review security logs
- [ ] Check SSL certificate validity
- [ ] Analyze website traffic
- [ ] Optimize database

#### Quarterly
- [ ] Security audit
- [ ] Performance review
- [ ] Update Django/packages
- [ ] Review backup integrity
- [ ] Business analytics review

#### Annually
- [ ] SSL certificate renewal
- [ ] Full security assessment
- [ ] Business review and planning
- [ ] Infrastructure upgrade evaluation

## Emergency Procedures

### If Website is Down
1. [ ] Check server status
2. [ ] Check application logs
3. [ ] Check database connection
4. [ ] Check disk space
5. [ ] Restart application service
6. [ ] Check Nginx status
7. [ ] Restore from backup if necessary

### If Database is Corrupted
1. [ ] Stop application
2. [ ] Restore from most recent backup
3. [ ] Verify data integrity
4. [ ] Restart application
5. [ ] Notify stakeholders

### If Server is Compromised
1. [ ] Take server offline
2. [ ] Take backups
3. [ ] Investigate security logs
4. [ ] Patch vulnerabilities
5. [ ] Restore from clean backup
6. [ ] Strengthen security measures

## Checklist Sign-off

- **Deployed By**: ________________
- **Date**: ________________
- **Environment**: ☐ Development  ☐ Staging  ☐ Production
- **All items completed**: ☐ Yes  ☐ No
- **Notes**: ________________________________

---

**Document Version**: 1.0
**Last Updated**: March 2024
**Next Review Date**: ________________
