from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_blog_content_and_inline_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(max_length=220, unique=True),
        ),
    ]
