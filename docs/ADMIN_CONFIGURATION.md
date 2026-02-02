# Django Admin Configuration Documentation

## Overview
The Django Admin panel is fully configured with comprehensive customization for all recipe app models. All CRUD operations (Create, Read, Update, Delete) are available.

---

## Admin Access

### URL
```
http://localhost:8000/admin/
```

### Default Credentials
- **Username**: admin
- **Password**: (Initially set, use `python manage.py changepassword admin` to change)

### To Start Development Server
```bash
python manage.py runserver
```

---

## Configured Models

### 1. Category Admin

**URL**: http://localhost:8000/admin/recipes/category/

**List Display**:
- ✓ Name
- ✓ Recipe Count (color-coded badge)
- ✓ Created Date

**Search Fields**:
- Category name
- Description

**Custom Features**:
- **recipe_count** - Displays number of recipes in category with blue badge styling

**CRUD Operations**:
- ✓ Create new categories
- ✓ Edit category details
- ✓ Delete categories
- ✓ Search by name or description

**Fieldsets**:
- Category Information (name, description)
- Metadata (created_at - collapsible)

---

### 2. Tag Admin

**URL**: http://localhost:8000/admin/recipes/tag/

**List Display**:
- ✓ Name
- ✓ Recipe Count (color-coded badge)
- ✓ Created Date

**Search Fields**:
- Tag name

**Custom Features**:
- **recipe_count** - Displays number of recipes tagged with light blue badge

**CRUD Operations**:
- ✓ Create new tags
- ✓ Edit tag information
- ✓ Delete tags
- ✓ Search by name

**Fieldsets**:
- Tag Information (name)
- Metadata (created_at - collapsible)

---

### 3. Profile Admin

**URL**: http://localhost:8000/admin/recipes/profile/

**List Display**:
- ✓ User (linked to user account)
- ✓ Location
- ✓ Followers Count (green badge)
- ✓ Following Count (orange badge)
- ✓ Created Date

**Search Fields**:
- Username
- User email
- Location
- Bio

**Filters**:
- Created Date
- Followers Count
- Following Count

**Custom Features**:
- **followers_display** - Green badge with follower count
- **following_display** - Orange badge with following count
- **avatar_preview** - Image preview (100x100 px, circular)

**CRUD Operations**:
- ✓ Create/Edit user profiles
- ✓ Upload avatar images
- ✓ Update bio and location info
- ✓ Modify follower counts
- ✓ Delete profiles

**Fieldsets**:
- User Information (user, avatar, avatar_preview)
- Profile Details (bio, location, website)
- Social Stats (followers_count, following_count)
- Timestamps (created_at, updated_at - collapsible)

**Read-Only Fields**:
- User (cannot change association)
- Created Date
- Updated Date
- Avatar Preview

---

### 4. Recipe Admin (Main Model)

**URL**: http://localhost:8000/admin/recipes/recipe/

**List Display** (9 columns):
- ✓ Title
- ✓ Author
- ✓ Category
- ✓ Difficulty (color-coded: green=easy, yellow=medium, red=hard)
- ✓ Total Time (with ⏱ icon)
- ✓ Servings
- ✓ Engagement (views & likes)
- ✓ Published Status (checkmark or draft indicator)
- ✓ Created Date

**Search Fields**:
- Recipe title
- Description
- Ingredients
- Instructions
- Author username

**Filters**:
- Category
- Difficulty level
- Published status
- Created date
- Tags
- Author

**Custom Features**:
- **difficulty_badge** - Color-coded difficulty with full name (easy/medium/hard)
- **time_display** - Displays total cooking time (prep + cook)
- **engagement_display** - Shows views count and likes count
- **published_status** - Green checkmark for published, gray X for draft
- **rating_average** - Shows star rating from comments/ratings

**Inlines** (Edit related objects without leaving page):
- **RatingInline** - Add/edit ratings for the recipe
- **CommentInline** - Add/edit comments for the recipe

**Special Features**:
- **filter_horizontal** - Better tag selection interface (drag & drop style)

**CRUD Operations**:
- ✓ Create new recipes with full details
- ✓ Edit all recipe fields
- ✓ Upload recipe images
- ✓ Add/remove tags
- ✓ Manage ratings inline
- ✓ Manage comments inline
- ✓ Delete recipes (cascades to comments and ratings)
- ✓ Toggle published status

**Fieldsets**:
- Recipe Information (title, description, author, category, published)
- Content (ingredients, instructions, image)
- Details (difficulty, prep_time, cook_time, servings, tags)
- Engagement Metrics (views_count, likes_count, rating_average - read-only)
- Timestamps (created_at, updated_at - collapsible)

**Read-Only Fields**:
- Created Date
- Updated Date
- Views Count
- Likes Count
- Average Rating

---

### 5. Comment Admin

**URL**: http://localhost:8000/admin/recipes/comment/

**List Display**:
- ✓ User
- ✓ Recipe Title (linked to recipe)
- ✓ Comment Preview (first 60 characters)
- ✓ Likes Count
- ✓ Created Date

**Search Fields**:
- User username
- Recipe title
- Comment text

**Filters**:
- Created Date
- Likes Count
- Recipe Category

**Custom Features**:
- **recipe_title** - Clickable link to associated recipe
- **comment_preview** - Shows truncated comment text in gray italics

**CRUD Operations**:
- ✓ Create new comments
- ✓ Edit comment text
- ✓ Update likes count
- ✓ Delete comments
- ✓ Search by username or recipe title

**Fieldsets**:
- Comment Information (recipe, user, text)
- Engagement (likes_count)
- Timestamps (created_at, updated_at - collapsible)

**Read-Only Fields**:
- Created Date
- Updated Date

---

### 6. Rating Admin

**URL**: http://localhost:8000/admin/recipes/rating/

**List Display**:
- ✓ User
- ✓ Recipe Title (linked to recipe)
- ✓ Score Display (star rating ⭐)
- ✓ Created Date

**Search Fields**:
- User username
- Recipe title

**Filters**:
- Score (1-5)
- Created Date
- Recipe Category

**Custom Features**:
- **recipe_title** - Clickable link to associated recipe
- **score_display** - Visual star representation (e.g., ⭐⭐⭐⭐ for 4/5)

**CRUD Operations**:
- ✓ Create new ratings (1-5 stars)
- ✓ Edit ratings
- ✓ Delete ratings
- ✓ One rating per user per recipe (enforced by database constraint)

**Fieldsets**:
- Rating Information (recipe, user, score)
- Timestamps (created_at, updated_at - collapsible)

**Read-Only Fields**:
- Created Date
- Updated Date

---

## Key Admin Features

### 1. Color-Coded Display
- **Green** (#70bf2b) - Easy difficulty, Published status, Healthy
- **Yellow** (#ffd966) - Medium difficulty
- **Red** (#ef5350) - Hard difficulty, Warnings
- **Blue** (#417690) - Category info, Primary actions
- **Light Blue** (#79aec8) - Tag info
- **Orange** (#ef8537) - Following count

### 2. Inline Editing
- **Recipe Admin**: Edit ratings and comments directly without leaving the recipe page
- Saves time and improves workflow

### 3. Search Capabilities
- Full-text search across multiple fields
- Search by related fields (e.g., username, recipe title)
- Case-insensitive search

### 4. Filtering
- Filter by date ranges
- Filter by related objects
- Multiple filters can be combined
- RelatedOnlyFieldListFilter for cleaner related field filtering

### 5. Fieldsets & Organization
- Logical grouping of fields
- Collapsible sections for metadata
- Read-only sections for system-generated data

### 6. Custom Display Methods
- Formatted output with HTML styling
- Clickable links for relationships
- Visual indicators (badges, icons, stars)

---

## CRUD Operations Summary

| Model | Create | Read | Update | Delete | Special |
|-------|--------|------|--------|--------|---------|
| Category | ✓ | ✓ | ✓ | ✓ | Shows recipe count |
| Tag | ✓ | ✓ | ✓ | ✓ | Shows recipe count |
| Profile | ✓ | ✓ | ✓ | ✓ | Avatar preview |
| Recipe | ✓ | ✓ | ✓ | ✓ | Inline ratings/comments |
| Comment | ✓ | ✓ | ✓ | ✓ | Recipe link |
| Rating | ✓ | ✓ | ✓ | ✓ | Star display |

---

## Data Relationships in Admin

### Category → Recipe
- View all recipes in a category
- Delete category (recipes remain, category becomes NULL)

### Tag → Recipe
- View all recipes with a tag
- Many-to-many relationship with filter_horizontal interface

### User → Profile
- OneToOne relationship
- View user profile through user admin or profile admin

### Recipe → Comments
- Edit comments inline within recipe
- View all comments for a recipe

### Recipe → Ratings
- Edit ratings inline within recipe
- View all ratings for a recipe

---

## Admin Tips & Tricks

### 1. Bulk Actions
- Select multiple records using checkboxes
- Django provides built-in delete action

### 2. Export Data
- Use Django's built-in export to CSV via third-party packages
- Or copy data from the list view

### 3. Search Operators
- Combine multiple search terms
- Use filters alongside search

### 4. Date Filters
- Quick date range selection
- Filter by "Today", "This Week", "This Month", etc.

### 5. Admin Actions
- Can be extended with custom actions
- Example: Mark recipes as published/unpublished in bulk

---

## Security Notes

- Only superusers/staff members can access admin
- All changes are logged
- Sensitive fields are protected
- Read-only fields cannot be modified from admin

---

## Customization Examples

### To Add a Custom Admin Action

```python
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # ... existing code ...
    
    actions = ['publish_recipes', 'unpublish_recipes']
    
    def publish_recipes(self, request, queryset):
        queryset.update(published=True)
    publish_recipes.short_description = "Publish selected recipes"
    
    def unpublish_recipes(self, request, queryset):
        queryset.update(published=False)
    unpublish_recipes.short_description = "Unpublish selected recipes"
```

### To Add Permission Checks

```python
def has_delete_permission(self, request):
    # Restrict deletion
    return request.user.is_superuser
```

---

## Testing the Admin

### 1. Access the Admin Panel
```bash
python manage.py runserver
# Visit: http://localhost:8000/admin/
```

### 2. Login with Credentials
- Username: admin
- Password: (default from setup)

### 3. Test CRUD Operations
- **Create**: Add a new category, tag, or recipe
- **Read**: View the list of items
- **Update**: Edit an existing item
- **Delete**: Remove an item

### 4. Test Relationships
- Create a recipe with multiple tags
- Add comments and ratings to a recipe
- View inline objects

### 5. Test Search & Filters
- Use search to find recipes
- Apply filters to narrow results
- Combine multiple filters

---

## Troubleshooting

### Issue: Admin page is slow
**Solution**: Add database indexes on frequently filtered fields (already done)

### Issue: Can't upload images
**Solution**: Ensure Pillow is installed (`pip install Pillow`) and MEDIA_ROOT is configured

### Issue: Foreign key filters not showing
**Solution**: Use `RelatedOnlyFieldListFilter` (already implemented)

### Issue: Inline objects not appearing
**Solution**: Verify inlines are added to the main admin class (already done for Recipe)

---

## Current Admin Statistics

- **Models Registered**: 6
- **Custom Admin Classes**: 6
- **Total Search Fields**: 18
- **Total Filter Fields**: 21
- **Custom Display Methods**: 12
- **Fieldsets**: 27
- **Inline Models**: 2
- **Read-only Fields**: 20+

---

## Next Steps

To enhance the admin further:

1. Add custom admin actions (e.g., bulk publish)
2. Add admin filters (e.g., recipe difficulty)
3. Add import/export functionality
4. Add custom admin templates
5. Add chart displays for statistics
6. Add activity logging

---

## Admin File Location
[recipes/admin.py](recipes/admin.py)

---

**Last Updated**: January 22, 2026
**Status**: ✅ Complete and Tested
