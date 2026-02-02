# Quick Reference: Django Models & Database

## Files Modified/Created

### Core Files
- **[recipes/models.py](recipes/models.py)** - All 6 models with enhanced fields
- **recipes/migrations/0001_initial.py** - Initial model creation
- **recipes/migrations/0002_alter_category_options_alter_comment_options_and_more.py** - Migration with all enhancements

### Database Files
- **db.sqlite3** - SQLite database with all tables and sample data
- **populate.py** - Script to populate sample data (updated with new fields)

### Documentation & Tools
- **[DATABASE_SUMMARY.md](DATABASE_SUMMARY.md)** - Comprehensive summary
- **verify_database.py** - Database verification script
- **schema_explorer.py** - Detailed schema viewer

---

## Quick Model Reference

### Category
```python
Category.objects.create(
    name='Italian',
    description='Italian cuisine'
)
```

### Tag
```python
Tag.objects.create(name='Vegetarian')
```

### Profile
```python
Profile.objects.create(
    user=user,
    bio='I love cooking!',
    location='New York',
    website='https://example.com'
)
```

### Recipe (Main Model)
```python
Recipe.objects.create(
    author=user,
    title='Pasta Carbonara',
    description='Classic Italian pasta',
    ingredients='Pasta\nEggs\nBacon',
    instructions='Mix and cook',
    category=category,
    prep_time=10,
    cook_time=20,
    servings=2,
    difficulty='easy'  # or 'medium', 'hard'
)
recipe.tags.add(tag1, tag2)
```

### Comment
```python
Comment.objects.create(
    recipe=recipe,
    user=user,
    text='Delicious recipe!'
)
```

### Rating
```python
Rating.objects.create(
    recipe=recipe,
    user=user,
    score=5  # 1-5
)
```

---

## Database Statistics

| Entity | Count |
|--------|-------|
| Users | 4 |
| Profiles | 3 |
| Categories | 6 |
| Tags | 6 |
| Recipes | 13 |
| Comments | 1 |
| Ratings | 1 |

---

## Sample Data Categories

1. **Italian** - Classic Spaghetti Carbonara
2. **Mexican** - Chicken Tacos
3. **Desserts** - Chocolate Chip Cookies
4. **Asian** - Pad Thai
5. **Breakfast** - Avocado Toast
6. **Healthy** - Grilled Salmon

---

## Useful Django Shell Commands

```bash
# Launch Django shell
python manage.py shell

# Get all recipes
from recipes.models import Recipe
Recipe.objects.all()

# Get recipes by author
recipe.Recipe.objects.filter(author__username='chef_mario')

# Get recipes by category
Recipe.objects.filter(category__name='Italian')

# Get recipes with specific tag
Recipe.objects.filter(tags__name='Vegetarian')

# Get average rating
recipe.get_average_rating()

# Get total time
recipe.get_total_time()

# Get recipe comments
recipe.comments.all()

# Get recipe ratings
recipe.ratings.all()
```

---

## Database Table Structure

### 7 Main Tables
- `recipes_category` - Recipe categories
- `recipes_tag` - Recipe tags
- `recipes_profile` - Extended user profiles
- `recipes_recipe` - Main recipe table
- `recipes_recipe_tags` - M2M relationship between recipes and tags
- `recipes_comment` - User comments on recipes
- `recipes_rating` - User ratings for recipes

### Key Features
✓ Proper CASCADE and SET_NULL delete behaviors
✓ Unique constraints on name fields
✓ Composite unique key on (recipe, user) for ratings
✓ Performance indexes on frequently queried fields
✓ Timestamp tracking (created_at, updated_at)

---

## Verification

Run these commands to verify everything:

```bash
# Check migrations
python manage.py showmigrations recipes

# View complete schema
python schema_explorer.py

# Verify database
python verify_database.py

# Query in shell
python manage.py shell
```

---

## Next Steps

To extend the models, you can:

1. **Add more fields** to existing models
2. **Create new models** for additional functionality
3. **Add methods** for calculated fields
4. **Create signals** for automatic actions
5. **Add validators** for data integrity

All changes require new migrations:
```bash
python manage.py makemigrations recipes
python manage.py migrate
```
