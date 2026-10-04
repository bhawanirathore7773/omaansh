import os
from pathlib import Path

import dj_database_url
from decouple import config
from django.templatetags.static import static
from django.urls import reverse_lazy


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-hoovale-development-key-change-in-production",
)
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "ALLOWED_HOSTS",
        default="localhost,127.0.0.1,www.hoovale.com,hoovale.com",
    ).split(",")
    if host.strip()
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "crispy_forms",
    "crispy_bootstrap5",
    "products",
    "enquiries",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "hoovale.middleware.CanonicalHostMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hoovale.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hoovale.wsgi.application"


# Cache — lightweight and free; safe for a single Render free web service.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "hoovale-cache",
        "TIMEOUT": 60 * 15,
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = "hoovale"
CACHE_MIDDLEWARE_SECONDS = 60 * 15

# Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

# Security
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool
)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config(
    "SECURE_CONTENT_TYPE_NOSNIFF", default=False, cast=bool
)
SECURE_BROWSER_XSS_FILTER = config(
    "SECURE_BROWSER_XSS_FILTER", default=False, cast=bool
)
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_REFERRER_POLICY = "same-origin"
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)

# Database
DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default="sqlite:///db.sqlite3")
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static / media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# ============================================================
# OTP / PASSWORD RECOVERY
# ============================================================
ADMIN_RESET_PHONE = config("ADMIN_RESET_PHONE", default="")
ADMIN_RESET_USERNAME = config("ADMIN_RESET_USERNAME", default="admin")

# Free email provider: Brevo transactional email.
# Set OTP_EMAIL_PROVIDER=console only for development/testing.
OTP_EMAIL_PROVIDER = config("OTP_EMAIL_PROVIDER", default="brevo")
BREVO_API_KEY = config("BREVO_API_KEY", default="")
BREVO_SENDER_EMAIL = config("BREVO_SENDER_EMAIL", default="")
BREVO_SENDER_NAME = config("BREVO_SENDER_NAME", default="HOOVALE")

# SMS provider: Twilio Verify for real SMS; console is a zero-cost local test mode.
OTP_SMS_PROVIDER = config("OTP_SMS_PROVIDER", default="twilio")
TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default="")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default="")
TWILIO_VERIFY_SERVICE_SID = config("TWILIO_VERIFY_SERVICE_SID", default="")


# ============================================================
# EXISTING WHATSAPP CONFIG — kept configurable, no hard-coded secrets
# ============================================================
OWNER_WHATSAPP_NUMBER = config("OWNER_WHATSAPP_NUMBER", default="919462207356")
ULTRAMSG_TOKEN = config("ULTRAMSG_TOKEN", default="")
ULTRAMSG_INSTANCE_ID = config("ULTRAMSG_INSTANCE_ID", default="")


# Logging
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "django.log",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


# Professional HOOVALE admin configuration
UNFOLD = {
    "SITE_TITLE": "HOOVALE Admin",
    "SITE_HEADER": "HOOVALE",
    "SITE_SUBHEADER": "Website Management",
    "SITE_URL": "/",
    "SITE_SYMBOL": "schedule",
    "SITE_LOGO": lambda request: static("images/hoovale-mark.svg"),
    "SITE_ICON": lambda request: static("images/hoovale-mark.svg"),
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "SHOW_UI_WARNINGS": False,
    "THEME": "light",
    "BORDER_RADIUS": "10px",
    "DASHBOARD_CALLBACK": "hoovale.admin_dashboard.dashboard_callback",
    "STYLES": [
        lambda request: static("css/hoovale-admin.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/hoovale-admin.js"),
    ],
}

UNFOLD["SIDEBAR"] = {
    "show_search": True,
    "show_all_applications": False,
    "navigation": [
        {
            "title": "Overview",
            "separator": True,
            "collapsible": False,
            "items": [
                {"title": "Dashboard", "icon": "dashboard", "link": "/admin/"},
                {"title": "View Website", "icon": "language", "link": "/"},
            ],
        },
        {
            "title": "Website Content",
            "separator": True,
            "collapsible": True,
            "items": [
                {"title": "Products", "icon": "inventory_2", "link": reverse_lazy("admin:products_product_changelist")},
                {"title": "Categories", "icon": "category", "link": reverse_lazy("admin:products_category_changelist")},
                {"title": "Services", "icon": "design_services", "link": reverse_lazy("admin:products_servicepage_changelist")},
                {"title": "Banners", "icon": "image", "link": reverse_lazy("admin:products_banner_changelist")},
                {"title": "Blog", "icon": "article", "link": reverse_lazy("admin:products_blog_changelist")},
                {"title": "FAQs", "icon": "help", "link": reverse_lazy("admin:products_faq_changelist")},
                {"title": "Testimonials", "icon": "reviews", "link": reverse_lazy("admin:products_testimonial_changelist")},
            ],
        },
        {
            "title": "SEO & Growth",
            "separator": True,
            "collapsible": True,
            "items": [
                {"title": "City Pages", "icon": "location_city", "link": reverse_lazy("admin:products_citypage_changelist")},
                {"title": "Industry Pages", "icon": "business", "link": reverse_lazy("admin:products_industrypage_changelist")},
                {"title": "Pricing Templates", "icon": "sell", "link": reverse_lazy("admin:products_pricingtiertemplate_changelist")},
                {"title": "Site & SEO Settings", "icon": "settings", "link": reverse_lazy("admin:products_sitesettings_changelist")},
            ],
        },
        {
            "title": "Leads",
            "separator": True,
            "collapsible": True,
            "items": [
                {"title": "Enquiries", "icon": "contact_mail", "link": reverse_lazy("admin:enquiries_enquiry_changelist")},
            ],
        },
        {
            "title": "Administration",
            "separator": True,
            "collapsible": True,
            "items": [
                {"title": "Users", "icon": "people", "link": reverse_lazy("admin:auth_user_changelist")},
                {"title": "Groups", "icon": "group", "link": reverse_lazy("admin:auth_group_changelist")},
            ],
        },
    ],
}
