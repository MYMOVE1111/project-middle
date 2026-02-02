#!/usr/bin/env python
"""
Schema Explorer - Displays complete database schema for all recipe app tables
"""

import os
import django
import sqlite3
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_sharing.settings')
django.setup()

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("\n" + "="*80)
print("DJANGO RECIPE-SHARING DATABASE SCHEMA".center(80))
print("="*80)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

recipe_tables = [
    'recipes_category',
    'recipes_tag',
    'recipes_profile',
    'recipes_recipe',
    'recipes_recipe_tags',
    'recipes_comment',
    'recipes_rating'
]

for table_name in recipe_tables:
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    print(f"\n📋 TABLE: {table_name}")
    print("-" * 80)
    print(f"{'Column Name':<25} {'Type':<20} {'Properties':<35}")
    print("-" * 80)
    
    for col in columns:
        col_id, col_name, col_type, not_null, default, pk = col
        properties = []
        
        if pk:
            properties.append("PRIMARY KEY")
        if not_null:
            properties.append("NOT NULL")
        if default:
            properties.append(f"DEFAULT: {default}")
        
        prop_str = ", ".join(properties) if properties else ""
        print(f"{col_name:<25} {col_type:<20} {prop_str:<35}")
    
    # Show indexes
    cursor.execute(f"PRAGMA index_list({table_name});")
    indexes = cursor.fetchall()
    if indexes:
        print(f"\n  Indexes:")
        for idx in indexes:
            idx_name = idx[1]
            cursor.execute(f"PRAGMA index_info({idx_name});")
            idx_cols = cursor.fetchall()
            cols_str = ", ".join([f"{col[2]}" for col in idx_cols])
            print(f"    - {idx_name}: ({cols_str})")

# Show foreign keys
print("\n" + "="*80)
print("FOREIGN KEY RELATIONSHIPS")
print("="*80)

fk_info = {
    'recipes_profile': [('user_id', 'auth_user', 'id', 'CASCADE')],
    'recipes_recipe': [
        ('author_id', 'auth_user', 'id', 'CASCADE'),
        ('category_id', 'recipes_category', 'id', 'SET_NULL')
    ],
    'recipes_comment': [
        ('recipe_id', 'recipes_recipe', 'id', 'CASCADE'),
        ('user_id', 'auth_user', 'id', 'CASCADE')
    ],
    'recipes_rating': [
        ('recipe_id', 'recipes_recipe', 'id', 'CASCADE'),
        ('user_id', 'auth_user', 'id', 'CASCADE')
    ],
    'recipes_recipe_tags': [
        ('recipe_id', 'recipes_recipe', 'id', 'CASCADE'),
        ('tag_id', 'recipes_tag', 'id', 'CASCADE')
    ]
}

for table, fks in fk_info.items():
    print(f"\n{table}:")
    for fk_col, ref_table, ref_col, behavior in fks:
        print(f"  {fk_col} → {ref_table}.{ref_col} (ON DELETE: {behavior})")

# Data Statistics
print("\n" + "="*80)
print("DATA STATISTICS")
print("="*80)

from recipes.models import Category, Tag, Recipe, Profile, Comment, Rating
from django.contrib.auth.models import User

stats = {
    'Users': User.objects.count(),
    'Profiles': Profile.objects.count(),
    'Categories': Category.objects.count(),
    'Tags': Tag.objects.count(),
    'Recipes': Recipe.objects.count(),
    'Comments': Comment.objects.count(),
    'Ratings': Rating.objects.count(),
}

for name, count in stats.items():
    print(f"{name:<20} {count:>5} records")

# Recipe details sample
print("\n" + "="*80)
print("SAMPLE RECIPE DATA")
print("="*80)

sample_recipe = Recipe.objects.first()
if sample_recipe:
    print(f"\nRecipe: {sample_recipe.title}")
    print(f"  ID: {sample_recipe.id}")
    print(f"  Author: {sample_recipe.author.username}")
    print(f"  Category: {sample_recipe.category.name if sample_recipe.category else 'N/A'}")
    print(f"  Difficulty: {sample_recipe.difficulty}")
    print(f"  Prep Time: {sample_recipe.prep_time} mins")
    print(f"  Cook Time: {sample_recipe.cook_time} mins")
    print(f"  Total Time: {sample_recipe.get_total_time()} mins")
    print(f"  Servings: {sample_recipe.servings}")
    print(f"  Views: {sample_recipe.views_count}")
    print(f"  Likes: {sample_recipe.likes_count}")
    print(f"  Tags: {', '.join([t.name for t in sample_recipe.tags.all()]) or 'None'}")
    print(f"  Published: {sample_recipe.published}")
    print(f"  Created: {sample_recipe.created_at}")
    print(f"  Updated: {sample_recipe.updated_at}")

conn.close()

print("\n" + "="*80)
print("✅ SCHEMA EXPORT COMPLETE")
print("="*80 + "\n")
