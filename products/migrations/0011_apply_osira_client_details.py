from django.db import migrations


def apply_osira_site_settings(apps, schema_editor):
    SiteSettings = apps.get_model("products", "SiteSettings")
    settings = SiteSettings.objects.order_by("id").first()

    if settings is None:
        settings = SiteSettings()

    # Only replace the legacy/default identity. If an administrator has already
    # entered a different live identity, preserve it.
    legacy_identity = (
        not settings.pk
        or not settings.business_name
        or settings.business_name.strip().upper() == "HOOVALE"
        or "hoovale" in (settings.email or "").lower()
    )
    if not legacy_identity:
        return

    values = {
        "business_name": "OSIRA",
        "tagline": "Thoughtfully crafted wall clocks and décor for modern spaces",
        "primary_phone": "+91141616961",
        "whatsapp_number": "919509912556",
        "email": "hello@omaansh.com",
        "street_address": "24, Shree Shyam Vatika, Gokulpura, Kalwar Road, Jaipur, Rajasthan 302012",
        "locality": "Gokulpura, Jaipur",
        "region": "Rajasthan",
        "postal_code": "302012",
        "country": "IN",
        "latitude": 26.9312482,
        "longitude": 75.7159318,
        "establishment_year": 2021,
        "employee_count": "10",
        "gst_number": "08BVNPS9491J1ZG",
        "default_meta_title": "OSIRA | Wall Clock Manufacturer & Supplier in Jaipur",
        "default_meta_description": "OSIRA creates wall clocks and décor products for homes, workplaces and commercial spaces, with custom and business order support.",
    }

    for field, value in values.items():
        setattr(settings, field, value)

    settings.save()


def reverse_osira_site_settings(apps, schema_editor):
    # Intentionally do not restore the legacy HOOVALE identity. A reverse
    # migration must not unexpectedly reintroduce an old brand into production.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0010_alter_blog_slug"),
    ]

    operations = [
        migrations.RunPython(
            apply_osira_site_settings,
            reverse_osira_site_settings,
        ),
    ]
