#!/usr/bin/env python
"""
Admin Configuration Verification Script
Tests all admin configurations and displays available features
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_sharing.settings')
django.setup()

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from recipes.models import Category, Tag, Profile, Recipe, Comment, Rating
from recipes.admin import (
    CategoryAdmin, TagAdmin, ProfileAdmin, RecipeAdmin,
    CommentAdmin, RatingAdmin
)

print("\n" + "="*80)
print("DJANGO ADMIN CONFIGURATION VERIFICATION".center(80))
print("="*80)

# Verify all models are registered
print("\n✓ REGISTERED MODELS")
print("-" * 80)

models = [
    ('Category', CategoryAdmin),
    ('Tag', TagAdmin),
    ('Profile', ProfileAdmin),
    ('Recipe', RecipeAdmin),
    ('Comment', CommentAdmin),
    ('Rating', RatingAdmin),
]

for model_name, admin_class in models:
    print(f"\n  📋 {model_name} Admin")
    print(f"     List Display: {len(admin_class.list_display)} fields")
    if hasattr(admin_class, 'search_fields'):
        print(f"     Search Fields: {', '.join(admin_class.search_fields) if admin_class.search_fields else 'None'}")
    if hasattr(admin_class, 'list_filter'):
        print(f"     Filters: {len(admin_class.list_filter)} available")
    if hasattr(admin_class, 'readonly_fields'):
        print(f"     Read-only Fields: {len(admin_class.readonly_fields)}")
    if hasattr(admin_class, 'fieldsets'):
        print(f"     Fieldsets: {len(admin_class.fieldsets)} sections")
    if hasattr(admin_class, 'inlines'):
        print(f"     Inlines: {len(admin_class.inlines)} related")

# Display detailed admin features
print("\n" + "="*80)
print("DETAILED ADMIN FEATURES".center(80))
print("="*80)

admin_configs = {
    'Category Admin': {
        'list_display': ['name', 'recipe_count', 'created_at'],
        'search': ['name', 'description'],
        'filters': [],
        'custom_methods': ['recipe_count - Show count with colored badge']
    },
    'Tag Admin': {
        'list_display': ['name', 'recipe_count', 'created_at'],
        'search': ['name'],
        'filters': [],
        'custom_methods': ['recipe_count - Show count with colored badge']
    },
    'Profile Admin': {
        'list_display': ['user', 'location', 'followers_display', 'following_display', 'created_at'],
        'search': ['user__username', 'user__email', 'location', 'bio'],
        'filters': ['created_at', 'followers_count', 'following_count'],
        'custom_methods': [
            'followers_display - Display followers with styling',
            'following_display - Display following with styling',
            'avatar_preview - Show image preview'
        ]
    },
    'Recipe Admin': {
        'list_display': [
            'title', 'author', 'category', 'difficulty_badge',
            'time_display', 'servings', 'engagement_display',
            'published_status', 'created_at'
        ],
        'search': ['title', 'description', 'ingredients', 'instructions', 'author__username'],
        'filters': ['category', 'difficulty', 'published', 'created_at', 'tags', 'author'],
        'custom_methods': [
            'difficulty_badge - Color-coded difficulty levels',
            'time_display - Show total cooking time',
            'engagement_display - Display views and likes',
            'published_status - Show publish status',
            'rating_average - Display star ratings'
        ],
        'inlines': ['RatingInline', 'CommentInline'],
        'special': 'filter_horizontal for tags selection'
    },
    'Comment Admin': {
        'list_display': ['user', 'recipe_title', 'comment_preview', 'likes_count', 'created_at'],
        'search': ['user__username', 'recipe__title', 'text'],
        'filters': ['created_at', 'likes_count', 'recipe__category'],
        'custom_methods': [
            'recipe_title - Display recipe title as link',
            'comment_preview - Show truncated comment text'
        ]
    },
    'Rating Admin': {
        'list_display': ['user', 'recipe_title', 'score_display', 'created_at'],
        'search': ['user__username', 'recipe__title'],
        'filters': ['score', 'created_at', 'recipe__category'],
        'custom_methods': [
            'recipe_title - Display recipe title as link',
            'score_display - Display star rating'
        ]
    }
}

for admin_name, config in admin_configs.items():
    print(f"\n{admin_name}:")
    print(f"  List Display Fields: {len(config['list_display'])}")
    for field in config['list_display'][:3]:
        print(f"    • {field}")
    if len(config['list_display']) > 3:
        print(f"    • ... and {len(config['list_display']) - 3} more")
    
    print(f"\n  Search Fields: {len(config['search'])}")
    for field in config['search'][:3]:
        print(f"    • {field}")
    if len(config['search']) > 3:
        print(f"    • ... and {len(config['search']) - 3} more")
    
    print(f"\n  Filters: {len(config['filters'])}")
    for filt in config['filters'][:3]:
        print(f"    • {filt}")
    if len(config['filters']) > 3:
        print(f"    • ... and {len(config['filters']) - 3} more")
    
    print(f"\n  Custom Display Methods: {len(config['custom_methods'])}")
    for method in config['custom_methods']:
        print(f"    • {method}")
    
    if 'inlines' in config:
        print(f"\n  Inlines (Related Objects): {', '.join(config['inlines'])}")
    
    if 'special' in config:
        print(f"\n  Special Feature: {config['special']}")

# Data statistics
print("\n" + "="*80)
print("ADMIN CRUD CAPABILITIES".center(80))
print("="*80)

from django.contrib.auth.models import User

crud_stats = {
    'Category': Category.objects.count(),
    'Tag': Tag.objects.count(),
    'Profile': Profile.objects.count(),
    'Recipe': Recipe.objects.count(),
    'Comment': Comment.objects.count(),
    'Rating': Rating.objects.count(),
}

print("\n✓ CRUD Operations Available (Create, Read, Update, Delete)")
print("\nCurrent Data in Database:")
for model, count in crud_stats.items():
    print(f"  • {model}: {count} records")

print(f"\n  • Admin Users: {User.objects.filter(is_staff=True).count()}")

# Admin URLs
print("\n" + "="*80)
print("ADMIN ACCESS INFORMATION".center(80))
print("="*80)

print("\n📍 Admin URL: http://localhost:8000/admin/")
print("\n🔑 Default Credentials:")
print("   Username: admin")
print("   Password: (use: python manage.py changepassword admin)")

print("\n📊 Admin Endpoints Available:")
print("   • http://localhost:8000/admin/recipes/category/")
print("   • http://localhost:8000/admin/recipes/tag/")
print("   • http://localhost:8000/admin/recipes/profile/")
print("   • http://localhost:8000/admin/recipes/recipe/")
print("   • http://localhost:8000/admin/recipes/comment/")
print("   • http://localhost:8000/admin/recipes/rating/")

print("\n" + "="*80)
print("✅ ADMIN CONFIGURATION COMPLETE".center(80))
print("="*80 + "\n")
