import os

import django
from django.contrib.auth import get_user_model

from profiles.models import Profile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django.setup()

User = get_user_model()

username = "admin"
email = "admin@admin.com"
password = "admin"

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(
        username=username, email=email, password=password
    )
    Profile.objects.create(user=user)
    print(f"✅ Superuser {username} created and profile added.")
else:
    print(f"ℹ️ Superuser {username} exist")
