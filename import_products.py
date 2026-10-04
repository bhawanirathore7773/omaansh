import csv
import os
import django
import ast

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hoovale.settings")
django.setup()

from products.models import Product, Category

CSV_FILE = "hoovale_products_seo.csv"

with open(CSV_FILE, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:

        category = Category.objects.get(name=row['category'])

        Product.objects.create(
            name=row['name'],
            slug=row['slug'],
            category=category,
            description=row['description'],
            price=row['price'] if row['price'] else None,
            image=row['image'],
            short_description=row['short_description'],
            moq=row['moq'],
            size_options=ast.literal_eval(row['size_options']),
            material_options=ast.literal_eval(row['material_options']),
            color_options=ast.literal_eval(row['color_options']),
            meta_title=row['meta_title'],
            meta_description=row['meta_description'],
            meta_keywords=row['meta_keywords'],
            og_title=row['og_title'],
            og_description=row['og_description'],
            is_featured=row['is_featured'] == "True",
            is_active=row['is_active'] == "True"
        )

        print("Added:", row['name'])
