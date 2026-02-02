import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_sharing.settings')
django.setup()

from recipes.models import Category, Tag, Recipe, Profile, Comment, Rating
from django.contrib.auth.models import User

# Get database connection
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print("=" * 60)
print("DATABASE VERIFICATION REPORT")
print("=" * 60)

print("\n✓ DATABASE TABLES CREATED:")
for table in tables:
    print(f"  - {table[0]}")

print("\n" + "=" * 60)
print("DATA SUMMARY")
print("=" * 60)

print(f"\nCategories: {Category.objects.count()}")
for cat in Category.objects.all():
    print(f"  - {cat.name} ({cat.recipes.count()} recipes)")

print(f"\nTags: {Tag.objects.count()}")
for tag in Tag.objects.all():
    print(f"  - {tag.name} ({tag.recipes.count()} recipes)")

print(f"\nUsers: {User.objects.count()}")
for user in User.objects.filter(username__in=['chef_mario', 'cook_sarah']):
    print(f"  - {user.username}: {user.recipes.count()} recipes")

print(f"\nRecipes: {Recipe.objects.count()}")
for recipe in Recipe.objects.all()[:6]:
    avg_rating = recipe.get_average_rating()
    print(f"  - {recipe.title}")
    print(f"    Author: {recipe.author.username}")
    print(f"    Difficulty: {recipe.difficulty}")
    print(f"    Time: {recipe.prep_time}min prep + {recipe.cook_time}min cook = {recipe.get_total_time()} mins")
    print(f"    Servings: {recipe.servings}")
    print(f"    Tags: {', '.join([t.name for t in recipe.tags.all()])}")
    print()

print("=" * 60)
print("SCHEMA VERIFICATION")
print("=" * 60)

# Check Recipe table columns
cursor.execute("PRAGMA table_info(recipes_recipe);")
recipe_columns = cursor.fetchall()
print("\nRecipe Model Columns:")
for col in recipe_columns:
    print(f"  - {col[1]}: {col[2]}")

conn.close()
print("\n✓ Database verification complete!")
