# Django Admin Quick Reference Guide

## Quick Access

### Admin URL
```
http://localhost:8000/admin/
```

### Login Credentials
- **Username**: admin
- **Password**: (set during project setup)

---

## Models & Their Admin Endpoints

### 1. Category
**URL**: `/admin/recipes/category/`

**Quick Actions**:
- Click "Add Category" to create new
- Search by name or description
- Edit: Click category name
- Delete: Select → Delete button

**Key Fields**:
- Name (required)
- Description (optional)

---

### 2. Tag
**URL**: `/admin/recipes/tag/`

**Quick Actions**:
- Click "Add Tag" to create new
- Search by name
- Edit: Click tag name
- Delete: Select → Delete button

**Key Fields**:
- Name (required)

---

### 3. Profile
**URL**: `/admin/recipes/profile/`

**Quick Actions**:
- Filter by followers or following count
- Search by username or email
- View avatar preview
- Edit profile details

**Key Fields**:
- User (select from dropdown)
- Bio (text)
- Avatar (upload image)
- Location (text)
- Website (URL)
- Followers/Following counts

**Filters Available**:
- Created date
- Followers count
- Following count

---

### 4. Recipe (Main Management)
**URL**: `/admin/recipes/recipe/`

**Quick Actions**:
- Click "Add Recipe" to create new
- Search by title, description, ingredients, or author
- Edit: Click recipe title
- Delete: Select → Delete button
- Edit comments/ratings inline

**Key Fields**:
- Title (required)
- Description (required)
- Author (select from users)
- Category (select from categories)
- Ingredients (text with line breaks)
- Instructions (text with line breaks)
- Difficulty (easy/medium/hard)
- Prep time (in minutes)
- Cook time (in minutes)
- Servings (number)
- Tags (multi-select)
- Image (upload)
- Published (checkbox)

**Filters Available**:
- Category
- Difficulty level
- Published status
- Created date
- Tags
- Author

**Special Features**:
- View inline ratings
- View inline comments
- Colored difficulty badges
- Total time calculation
- Average rating display
- Engagement metrics (views, likes)

---

### 5. Comment
**URL**: `/admin/recipes/comment/`

**Quick Actions**:
- View all comments
- Search by username, recipe, or text
- Edit comment text or likes
- Delete comment

**Key Fields**:
- Recipe (select from dropdown)
- User (select from users)
- Text (required)
- Likes count

**Filters Available**:
- Created date
- Likes count
- Recipe category

---

### 6. Rating
**URL**: `/admin/recipes/rating/`

**Quick Actions**:
- View all ratings
- Search by username or recipe
- Edit rating score (1-5)
- Delete rating

**Key Fields**:
- Recipe (select from dropdown)
- User (select from users)
- Score (1-5 stars)

**Filters Available**:
- Score (1-5)
- Created date
- Recipe category

**Special Feature**: One rating per user per recipe (enforced)

---

## Common Admin Tasks

### Create a Recipe
1. Go to `/admin/recipes/recipe/`
2. Click "Add Recipe" button
3. Fill in required fields:
   - Title
   - Description
   - Author
   - Category
   - Ingredients
   - Instructions
4. Add optional details:
   - Prep/Cook time
   - Servings
   - Difficulty
   - Tags
   - Image
5. Click "Save"

### Search Recipes
1. Go to `/admin/recipes/recipe/`
2. Use search box to search by:
   - Title
   - Description
   - Ingredients
   - Instructions
   - Author username
3. Press Enter or click magnifying glass

### Filter Recipes
1. Go to `/admin/recipes/recipe/`
2. On the right side, use filters:
   - Select Category
   - Select Difficulty
   - Select Published status
   - Select Date range
3. Multiple filters work together

### Edit Recipe with Comments
1. Go to `/admin/recipes/recipe/`
2. Click recipe title to edit
3. Scroll down to see:
   - **Ratings** - Inline edit ratings
   - **Comments** - Inline edit comments
4. Add new or modify existing
5. Click "Save Recipe"

### Add Tag to Multiple Recipes
1. Go to `/admin/recipes/recipe/`
2. Click recipe title
3. In "Details" section, find "Tags"
4. Use dropdown to select tags
5. Click "Save"

### View Recipe Statistics
1. Go to `/admin/recipes/recipe/`
2. In list view, columns show:
   - Difficulty (color-coded)
   - Total time
   - Engagement (views + likes)
   - Publish status
   - Average rating

### Manage User Profiles
1. Go to `/admin/recipes/profile/`
2. Click username to edit profile
3. Can edit:
   - Bio
   - Avatar (upload image)
   - Location
   - Website URL
   - Follower/following counts

### Add Comment to Recipe
1. Go to `/admin/recipes/recipe/`
2. Click recipe title
3. Scroll to "Comments" section
4. Click "Add another Comment"
5. Select user and enter text
6. Click "Save Recipe"

### Add Rating to Recipe
1. Go to `/admin/recipes/recipe/`
2. Click recipe title
3. Scroll to "Ratings" section
4. Click "Add another Rating"
5. Select user and enter score (1-5)
6. Click "Save Recipe"

---

## Keyboard Shortcuts

### Admin Navigation
- **Tab** - Move between fields
- **Shift + Tab** - Move to previous field
- **Enter** - Save changes
- **Ctrl + A** - Select all items in list

### In List View
- **Checkbox** - Select individual item
- **Top checkbox** - Select all items on page
- **Delete button** - Delete selected items

---

## Display Customization

### Colored Badges Explained

**Difficulty Levels**:
- 🟢 **Green** = Easy
- 🟡 **Yellow** = Medium
- 🔴 **Red** = Hard

**Status Indicators**:
- ✓ **Green checkmark** = Published
- ✗ **Gray X** = Draft

**Social Counts**:
- 👥 **Green badge** = Followers
- 🔗 **Orange badge** = Following

---

## Tips & Tricks

### 1. Bulk Delete
- Check multiple items
- Select "Delete selected [items]" from action dropdown
- Confirm deletion

### 2. Filter by Date
- Click on date filter
- Select "Any date", "Today", "This week", "This month", etc.
- Or set custom date range

### 3. Combine Filters
- Select multiple filters
- They work together (AND logic)
- Clear filter by clicking "Clear all filters" link

### 4. Sort Columns
- Click on column header to sort
- Click again to reverse sort
- Currently sorted column shows arrow indicator

### 5. Import/Export
- Can copy data from list view
- Use browser's export features
- Or third-party admin extensions

### 6. View Related Objects
- Click on linked objects (recipe name, username, etc.)
- Takes you to that object's edit page
- Back button returns to previous view

---

## Common Filters

### Recipe Filters
```
Category → Select from dropdown
Difficulty → Easy, Medium, Hard
Published → Yes, No
Created date → Today, This week, This month
Tags → Multi-select
Author → Multi-select
```

### Comment Filters
```
Created date → Date range
Likes count → Greater than, Less than
Recipe category → Multi-select
```

### Rating Filters
```
Score → 1 star, 2 stars, 3 stars, 4 stars, 5 stars
Created date → Date range
Recipe category → Multi-select
```

### Profile Filters
```
Created date → Date range
Followers count → Numeric range
Following count → Numeric range
```

---

## Search Examples

### Search Recipes
```
"pasta" → Find recipes with "pasta" in title/description/ingredients
"author:chef_mario" → Find recipes by chef_mario
"carbonara" → Find recipe with that word
```

### Search Comments
```
"delicious" → Find comments with "delicious"
"admin" → Find comments about admin
```

### Search Profiles
```
"mario" → Find user with mario in username
"example.com" → Find user with that website
```

---

## Troubleshooting

### Can't find admin button?
- Check that you're logged in as admin/staff
- URL should be `/admin/`

### Can't upload image?
- Ensure Pillow is installed
- Check media folder permissions
- Verify image format (JPG, PNG, etc.)

### Inline objects not showing?
- Scroll down to find inline section
- May be below other fieldsets

### Filter not working?
- Check that field exists in model
- Try clearing all filters and reapply

### Search not finding items?
- Ensure search fields are configured
- Try different keywords
- Check exact spelling

---

## Frequently Used Buttons

| Button | Action |
|--------|--------|
| **Save** | Save changes and stay on page |
| **Save and continue editing** | Save and reload page |
| **Save and add another** | Save and create new item |
| **Delete** | Remove item (with confirmation) |
| **+ Add [Model]** | Create new item |
| **Clear all filters** | Remove all active filters |
| **Show filters** | Display filter sidebar |

---

## Admin Permissions

### Staff Permissions Required
- Access admin panel
- View any model
- Add, change, or delete records

### Superuser
- Full access to all models
- Can manage users and permissions
- Can access all admin features

### To change password
```bash
python manage.py changepassword admin
```

---

## Data Integrity Features

### Automatic Protection
- ✓ Unique constraints enforced
- ✓ Foreign key validation
- ✓ One rating per user per recipe
- ✓ CASCADE deletes configured
- ✓ Read-only fields protected

### Validation Examples
- Score must be 1-5
- Servings must be at least 1
- Required fields cannot be empty
- Unique names cannot duplicate

---

## Monitoring

### View Edit History
- Check "Last modified" timestamp
- See who created/updated record
- Django admin logs actions

### Check Relationships
- View recipe → see all comments/ratings
- View user → see all recipes/comments
- View category → see all recipes

---

## Next Steps

To extend admin further:
1. Add custom admin actions (bulk operations)
2. Add import/export functionality
3. Add advanced filters
4. Customize admin templates
5. Add charts/statistics dashboard

---

**Last Updated**: January 22, 2026
**Status**: ✅ Ready for Use

Visit `/admin/` to get started!
