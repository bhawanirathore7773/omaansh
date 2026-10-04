# Generated migration for Banner model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_blog'),  # Update this to your latest migration
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Banner title (for admin reference)', max_length=200)),
                ('banner_type', models.CharField(choices=[('website', 'Website Banner (Desktop)'), ('mobile', 'Mobile Banner')], default='website', help_text='Choose banner type', max_length=20)),
                ('image', models.ImageField(help_text='Banner image (Recommended: 1920x600px for desktop, 600x800px for mobile)', upload_to='banners/')),
                ('heading', models.CharField(blank=True, help_text='Main heading text', max_length=200)),
                ('subheading', models.CharField(blank=True, help_text='Subheading text', max_length=400)),
                ('cta_text', models.CharField(blank=True, help_text="Call-to-action button text (e.g., 'Shop Now')", max_length=100)),
                ('cta_url', models.CharField(blank=True, help_text='URL to redirect on button click', max_length=500)),
                ('text_color', models.CharField(default='#FFFFFF', help_text='Text color (hex code)', max_length=7)),
                ('text_position', models.CharField(choices=[('top-left', 'Top Left'), ('top-center', 'Top Center'), ('top-right', 'Top Right'), ('center-left', 'Center Left'), ('center-center', 'Center Center'), ('center-right', 'Center Right'), ('bottom-left', 'Bottom Left'), ('bottom-center', 'Bottom Center'), ('bottom-right', 'Bottom Right')], default='center-center', help_text='Text position on banner', max_length=20)),
                ('overlay_opacity', models.FloatField(default=0.3, help_text='Overlay darkness (0.0 to 1.0)')),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower number = shown first)')),
                ('is_active', models.BooleanField(default=True, help_text='Show this banner?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Banners',
            },
        ),
        migrations.AddIndex(
            model_name='banner',
            index=models.Index(fields=['banner_type', 'is_active'], name='products_ba_banner__idx'),
        ),
    ]
