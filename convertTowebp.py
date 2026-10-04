from PIL import Image
import os

MEDIA_DIR = 'media'

for root, dirs, files in os.walk(MEDIA_DIR):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(root, file)
            try:
                img = Image.open(path)
                webp_path = os.path.splitext(path)[0] + '.webp'
                img.save(webp_path, 'webp', quality=82, method=6)
                print(f'✓ {file} → WebP')
            except Exception as e:
                print(f'✗ {file}: {e}')