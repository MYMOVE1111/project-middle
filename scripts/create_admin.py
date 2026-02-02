import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_sharing.settings')
django.setup()

from django.contrib.auth.models import User

# Delete old admin
User.objects.filter(username='admin').delete()

# Create new admin
admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
print("✓ Админ создан: username=admin password=admin123")
