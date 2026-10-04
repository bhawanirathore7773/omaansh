import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hoovale.settings")
django.setup()

from products.models import Product

# image source
BASE_URL = "https://picsum.photos/800/600"

MEDIA_PATH = "media/products"

if not os.path.exists(MEDIA_PATH):
    os.makedirs(MEDIA_PATH)

products = Product.objects.all()

print("\nDownloading images for products...\n")

for product in products:
    
    filename = product.image.name.split("/")[-1]
    filepath = os.path.join(MEDIA_PATH, filename)

    if os.path.exists(filepath):
        print(f"✔ Already exists: {filename}")
        continue

    try:
        response = requests.get(BASE_URL)

        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"⬇ Downloaded: {filename}")

        else:
            print(f"❌ Failed: {filename}")

    except Exception as e:
        print("Error:", e)

print("\n✅ All images processed\n")