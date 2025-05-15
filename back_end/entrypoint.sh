#!/bin/bash

echo "👉 Migration"
python manage.py migrate --noinput

echo "👉 Create Super User"
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@admin.com", "admin")
EOF

echo "👉 Server start"
exec python manage.py runserver 0.0.0.0:8000
