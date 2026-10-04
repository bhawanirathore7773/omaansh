import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hoovale.settings")

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("ADMIN_USERNAME", "admin").strip()
email = os.environ.get("ADMIN_EMAIL", "admin@hoovale.com").strip()
password = os.environ.get("ADMIN_PASSWORD", "").strip()

if not password:
    raise RuntimeError("ADMIN_PASSWORD is not set. Add it in Render Environment Variables before deploying.")

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "email": email,
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
    },
)

if created:
    user.set_password(password)
    user.save()
    print(f"Created Django superuser: {username}")
else:
    changed = False
    if not user.is_staff:
        user.is_staff = True
        changed = True
    if not user.is_superuser:
        user.is_superuser = True
        changed = True
    if not user.is_active:
        user.is_active = True
        changed = True
    if email and user.email != email:
        user.email = email
        changed = True
    if changed:
        user.save()
    print(f"Superuser already exists: {username} (password was not reset)")
