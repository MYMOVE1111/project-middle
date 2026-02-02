import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_sharing.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Profile

# Get or create all users' profiles
users = User.objects.all()

for user in users:
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        print(f"✓ Profile created for user: {user.username}")
    else:
        print(f"✓ Profile already exists for user: {user.username}")
