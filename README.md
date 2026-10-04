# HOOVALE - Premium Wall Clock E-Commerce Website

A production-ready Django-based e-commerce website for HOOVALE, a premium wall clock manufacturer and wholesaler. This project includes a fully functional product catalog, enquiry management system, and modern responsive design.

## 🎯 Features

### Core Features
- ✅ Product catalog with advanced filtering and search
- ✅ Product detail pages with multiple images
- ✅ Enquiry management system with database storage
- ✅ WhatsApp integration for quick contact
- ✅ Category-based product organization
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Admin panel with full CRUD operations
- ✅ SEO optimized URLs and meta tags

### Technical Features
- ✅ Django admin panel for content management
- ✅ Lazy loading images for performance
- ✅ Sticky header navigation
- ✅ Modal-based enquiry forms
- ✅ Filter and search functionality
- ✅ Pagination for product lists
- ✅ WhatsApp floating button
- ✅ Sitemap for SEO
- ✅ Robots.txt configuration

## 📋 Project Structure

```
hoovale_project/
├── hoovale/                    # Django project settings
│   ├── settings.py            # Project configuration
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
│
├── products/                   # Products app
│   ├── models.py              # Product, Category, ProductImage models
│   ├── views.py               # Product views and handlers
│   ├── urls.py                # Products URLs
│   ├── admin.py               # Admin configuration
│   └── apps.py                # App configuration
│
├── enquiries/                  # Enquiries app
│   ├── models.py              # Enquiry model
│   ├── views.py               # Enquiry views
│   ├── urls.py                # Enquiry URLs
│   ├── admin.py               # Admin configuration
│   └── apps.py                # App configuration
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with header/footer
│   └── products/
│       ├── home.html          # Home page
│       ├── products_list.html  # Products listing
│       ├── product_detail.html # Product detail page
│       ├── about.html         # About page
│       ├── contact.html       # Contact page
│       ├── sitemap.xml        # Sitemap
│       ├── 404.html           # 404 error page
│       └── 500.html           # 500 error page
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main CSS file
│   ├── js/
│   │   └── main.js            # Main JavaScript
│   └── images/                # Image assets
│
├── media/                      # User uploaded files
│   ├── products/              # Product images
│   ├── categories/            # Category images
│   └── og_images/             # Open Graph images
│
├── logs/                       # Application logs
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── gunicorn_config.py          # Gunicorn configuration
├── pythonanywhere_wsgi.py      # PythonAnywhere WSGI
└── render.yaml                 # Render.com deployment config
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip package manager
- Virtual environment

### Local Development Setup

1. **Clone the repository**
```bash
cd hoovale_project
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser account**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server**
```bash
python manage.py runserver
```

9. **Access the website**
- Home: http://localhost:8000
- Admin: http://localhost:8000/admin

## 🛠️ Admin Panel Usage

### Adding Products

1. Login to admin: http://localhost:8000/admin
2. Go to Products → Products
3. Click "Add Product"
4. Fill in the details:
   - Name, Slug, Category
   - Description
   - Image (main)
   - Price (optional)
   - Customization options (Size, Material, Color)
   - SEO fields (Meta title, description, keywords)
   - Open Graph tags for social sharing
5. Save and view on frontend

### Managing Categories

1. Go to Products → Categories
2. Add new category with:
   - Name
   - Slug (auto-generated from name)
   - Description (optional)
   - Image (optional)

### Viewing Enquiries

1. Go to Enquiries → Enquiries
2. View all customer enquiries
3. Update status (New, Contacted, Interested, Converted, Lost)
4. Add internal notes
5. Read-only view of customer messages

## 📱 Responsive Design

The website is fully responsive and optimized for:
- **Desktop**: Full layout with sidebar filters
- **Tablet**: Optimized navigation and spacing
- **Mobile**: Stacked layout, mobile-friendly forms

## 🎨 Customization

### Changing Colors

Edit `/static/css/style.css` CSS variables:
```css
:root {
    --primary-color: #0051A3;        /* Royal Blue */
    --primary-dark: #003a78;
    --secondary-color: #ffffff;      /* White */
    --text-color: #333333;
    --text-light: #666666;
    --text-muted: #999999;
    --border-color: #e0e0e0;
    --bg-light: #f8f9fa;
}
```

### Changing WhatsApp Number

1. Update in `templates/base.html` floating button
2. Update in `templates/products/home.html` product actions
3. Update in `templates/products/products_list.html` product actions

### Custom Product Images

- Add placeholder images to `/static/images/`
- Update image paths in templates

## 🚢 Deployment

### PythonAnywhere

1. Upload project to PythonAnywhere
2. Create web app with Python 3.9+
3. Configure WSGI file (use `pythonanywhere_wsgi.py`)
4. Set up environment variables
5. Reload web app
6. Database: Use SQLite or configure PostgreSQL

**PythonAnywhere Setup Steps:**
```bash
# In PythonAnywhere bash console
mkvirtualenv hoovale --python=/usr/bin/python3.9
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### Render.com

1. Push code to GitHub
2. Connect GitHub repository to Render
3. Create new Web Service
4. Set environment variables
5. Deploy using `render.yaml`

**Environment Variables for Render:**
```
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=yourdomain.onrender.com
DATABASE_URL=postgresql://...
```

### VPS Server (Ubuntu/Debian)

1. **Install Python and dependencies**
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip
sudo apt install postgresql postgresql-contrib
```

2. **Setup project**
```bash
cd /var/www
sudo git clone your-repo hoovale_project
cd hoovale_project
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure database**
```bash
sudo -u postgres psql
CREATE DATABASE hoovale_db;
CREATE USER hoovale_user WITH PASSWORD 'secure_password';
ALTER ROLE hoovale_user SET client_encoding TO 'utf8';
ALTER ROLE hoovale_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE hoovale_db TO hoovale_user;
\q
```

4. **Update settings.py**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hoovale_db',
        'USER': 'hoovale_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Run migrations**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

6. **Setup Gunicorn and Nginx**
```bash
pip install gunicorn
# Create systemd service file
sudo nano /etc/systemd/system/hoovale.service
```

7. **Systemd service configuration**
```ini
[Unit]
Description=Hoovale Gunicorn Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/hoovale_project
ExecStart=/var/www/hoovale_project/venv/bin/gunicorn --config gunicorn_config.py hoovale.wsgi:application

[Install]
WantedBy=multi-user.target
```

8. **Setup Nginx reverse proxy**
```bash
sudo nano /etc/nginx/sites-available/hoovale
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/hoovale_project/staticfiles/;
    }

    location /media/ {
        alias /var/www/hoovale_project/media/;
    }
}
```

9. **Enable and start services**
```bash
sudo systemctl daemon-reload
sudo systemctl start hoovale
sudo systemctl enable hoovale
sudo systemctl restart nginx
```

## 📊 Database Models

### Product Model
- name, slug, category
- description, image
- price, size_options, material_options, color_options
- meta_title, meta_description, meta_keywords
- og_title, og_description, og_image
- is_featured, is_active
- created_at, updated_at

### Category Model
- name, slug, description
- image
- created_at, updated_at

### ProductImage Model
- product, image
- alt_text, is_primary
- created_at

### Enquiry Model
- product, name, phone
- email, city, message
- status (New, Contacted, Interested, Converted, Lost)
- notes, created_at, updated_at

## 🔒 Security Best Practices

1. **Change SECRET_KEY in production**
2. **Set DEBUG=False in production**
3. **Use HTTPS with valid SSL certificate**
4. **Set SECURE_SSL_REDIRECT=True**
5. **Configure ALLOWED_HOSTS with your domain**
6. **Use strong database password**
7. **Keep dependencies updated**
8. **Use environment variables for sensitive data**
9. **Regular backups of database and media files**
10. **Monitor logs for suspicious activity**

## 🔧 Maintenance

### Regular Backups
```bash
# Database backup
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Media files backup
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### Update Dependencies
```bash
pip list --outdated
pip install --upgrade package_name
```

### Clear Old Enquiries
Create management command or use Django shell:
```python
from enquiries.models import Enquiry
from django.utils import timezone
from datetime import timedelta

# Delete enquiries older than 1 year
old_date = timezone.now() - timedelta(days=365)
Enquiry.objects.filter(created_at__lt=old_date).delete()
```

## 📈 Performance Optimization

1. **Enable caching**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

2. **Database query optimization**
- Use select_related() for foreign keys
- Use prefetch_related() for reverse relations

3. **Image optimization**
- Compress images before upload
- Use appropriate image sizes
- Enable lazy loading

4. **CDN for static files**
- CloudFlare for static files and images

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
lsof -i :8000
kill -9 <PID>
```

### Database migration errors
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Permission denied on media files
```bash
chmod -R 755 media/
chmod -R 755 logs/
```

## 📞 Support Contact

For issues or questions:
- Email: info@hoovale.com
- Phone: +91-98765-43210
- WhatsApp: +91-98765-43210

## 📄 License

This project is proprietary and owned by HOOVALE. All rights reserved.

## 🎓 Documentation Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [PythonAnywhere Deployment](https://help.pythonanywhere.com/)
- [Render.com Documentation](https://render.com/docs/)

---

**Last Updated**: March 2024
**Version**: 1.0.0
**Status**: Production Ready
