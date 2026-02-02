#!/usr/bin/env python
"""
Script to reset admin password
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_sharing.settings')
django.setup()

from django.contrib.auth.models import User

# Сбросить пароль для админа
try:
    user = User.objects.get(username='admin')
    user.set_password('admin')
    user.save()
    print("✓ Пароль админа сброшен на: admin")
    print("  Username: admin")
    print("  Password: admin")
except User.DoesNotExist:
    print("✗ Пользователь 'admin' не найден")
    print("Создаем нового админа...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✓ Новый админ создан")
    print("  Username: admin")
    print("  Password: admin")
except Exception as e:
    print(f"✗ Ошибка: {e}")
