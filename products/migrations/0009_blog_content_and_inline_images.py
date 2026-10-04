from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_campaign_catalog_and_banner_pages'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content_html',
            field=models.TextField(blank=True, help_text='Optional article body HTML. Use headings, lists and links; keep content useful for readers.'),
        ),
        migrations.AddField(
            model_name='blog',
            name='inline_image_1',
            field=models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='inline_image_2',
            field=models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='inline_image_3',
            field=models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='inline_image_1_caption',
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.AddField(
            model_name='blog',
            name='inline_image_2_caption',
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.AddField(
            model_name='blog',
            name='inline_image_3_caption',
            field=models.CharField(blank=True, max_length=180),
        ),
    ]
