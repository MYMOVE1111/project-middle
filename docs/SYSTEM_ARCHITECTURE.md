# System Architecture Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Django Project Structure](#django-project-structure)
3. [Data Models](#data-models)
4. [Views & URL Routing](#views--url-routing)
5. [Templates](#templates)
6. [API Layer](#api-layer)
7. [Architecture Diagram](#architecture-diagram)

---

## Project Overview

**Project Name:** Recipe Sharing Platform  
**Framework:** Django 4.2 with Django REST Framework  
**Database:** SQLite3 (development) / PostgreSQL (production support)  
**Static Files:** WhiteNoise for production static file serving  
**Deployment:** Render.com compatible

### Technology Stack
- **Backend:** Django, Django REST Framework
- **Database:** SQLite3 / PostgreSQL
- **Frontend:** Django Templates (server-side rendering)
- **Static Files:** CSS, Images
- **Authentication:** Django built-in auth system
- **API:** RESTful API with DRF

---

## Django Project Structure

### Root-Level Configuration

```
project-middle/
├── recipe_sharing/          # Main Django project configuration
│   ├── settings.py          # Core project settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI application entry point
│   ├── asgi.py              # ASGI application entry point
│   └── __pycache__/
│
├── recipes/                 # Main Django app
│   ├── models.py            # All data models
│   ├── views.py             # Web views (HTML rendering)
│   ├── api_views.py         # API views (REST endpoints)
│   ├── serializers.py       # DRF serializers
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── tests.py             # Unit tests
│   ├── management/          # Django management commands
│   │   └── commands/
│   │       └── populate_recipes.py
│   └── migrations/          # Database migrations
│
├── templates/               # Template files
│   ├── base.html            # Base template
│   ├── recipes/             # Recipe-related templates
│   │   ├── home.html
│   │   ├── recipe_detail.html
│   │   ├── recipe_list.html
│   │   ├── create_recipe.html
│   │   ├── edit_recipe.html
│   │   ├── category_list.html
│   │   ├── category_detail.html
│   │   ├── tag_detail.html
│   │   ├── profile.html
│   │   └── edit_profile.html
│   └── registration/        # Authentication templates
│       ├── login.html
│       ├── logout.html
│       └── register.html
│
├── static/                  # Static files
│   ├── css/
│   │   ├── style.css
│   │   └── utilities.css
│   └── images/              # Static images
│
├── media/                   # User-uploaded files
│   ├── recipes/             # Recipe images
│   └── avatars/             # User avatars
│
├── scripts/                 # Utility scripts
├── manage.py                # Django management command
├── settings.py              # Settings file
├── requirements.txt         # Python dependencies
└── db.sqlite3               # Development database
```

### INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',           # Django admin interface
    'django.contrib.auth',            # User authentication
    'django.contrib.contenttypes',    # Content type framework
    'django.contrib.sessions',        # Session management
    'django.contrib.messages',        # Messaging framework
    'django.contrib.staticfiles',     # Static file management
    'rest_framework',                 # Django REST Framework
    'recipes',                        # Main application
]
```

---

## Data Models

### 1. User (Built-in Django Model)

**Description:** Extended Django User model for authentication and ownership

**Fields:**
- `username`: Unique username
- `email`: User email
- `password`: Hashed password
- `first_name`: User's first name
- `last_name`: User's last name

**Relationships:**
- One-to-Many with Recipe (author)
- One-to-Many with Comment
- One-to-Many with Rating
- One-to-One with Profile

---

### 2. Profile Model

**Purpose:** Extended user profile with additional social features

**Fields:**
```python
- user (OneToOne → User)      # Required relationship
- bio (TextField)              # User biography (max 500 chars)
- avatar (ImageField)          # Profile picture
- location (CharField)         # User location (max 100 chars)
- website (URLField)           # Personal website link
- followers_count (Integer)    # Number of followers
- following_count (Integer)    # Number of users following
- created_at (DateTime)        # Profile creation timestamp
- updated_at (DateTime)        # Last update timestamp
```

**Usage:** User profiles accessible at `/profile/<username>/`

---

### 3. Category Model

**Purpose:** Recipe categories for organization (e.g., Breakfast, Dessert, etc.)

**Fields:**
```python
- name (CharField)          # Unique category name (max 100 chars)
- description (TextField)   # Category description
- created_at (DateTime)     # Creation timestamp
```

**Relationships:**
- One-to-Many with Recipe (reverse: `recipes`)

**Ordering:** By name (A-Z)

---

### 4. Tag Model

**Purpose:** Tagging system for recipe attributes (e.g., Vegan, Gluten-Free)

**Fields:**
```python
- name (CharField)      # Unique tag name (max 50 chars)
- created_at (DateTime) # Creation timestamp
```

**Relationships:**
- Many-to-Many with Recipe (reverse: `recipes`)

**Ordering:** By name (A-Z)

---

### 5. Recipe Model (Core)

**Purpose:** Main content model storing recipe information

**Fields:**
```python
# Basic Information
- title (CharField)              # Recipe title (max 200 chars)
- description (TextField)        # Recipe description (max 1000 chars)
- ingredients (TextField)        # Comma-separated ingredient list
- instructions (TextField)       # Detailed cooking steps

# Relationships
- author (ForeignKey → User)     # Recipe creator
- category (ForeignKey → Category)  # Recipe category
- tags (ManyToMany → Tag)        # Multiple tags

# Cooking Details
- prep_time (Integer)            # Preparation time in minutes
- cook_time (Integer)            # Cooking time in minutes
- servings (Integer)             # Number of servings (min: 1)
- difficulty (CharField)         # Choices: easy, medium, hard

# Media
- image (ImageField)             # Recipe image

# Engagement
- views_count (Integer)          # Number of views
- likes_count (Integer)          # Number of likes

# Timestamps
- created_at (DateTime)          # Creation timestamp
- updated_at (DateTime)          # Last update timestamp
- published (Boolean)            # Publication status

# Metadata
- class Meta:
    ordering = ['-created_at']
    indexes = [
        Index(fields=['author', '-created_at']),
        Index(fields=['category', '-created_at']),
    ]
```

**Methods:**
- `get_total_time()`: Returns sum of prep_time and cook_time
- `get_average_rating()`: Calculates average rating from all ratings

**Relationships:**
- Many-to-One with User (reverse: `recipes`)
- Many-to-One with Category (reverse: `recipes`)
- Many-to-Many with Tag (reverse: `recipes`)
- One-to-Many with Comment (reverse: `comments`)
- One-to-Many with Rating (reverse: `ratings`)

---

### 6. Comment Model

**Purpose:** User comments on recipes

**Fields:**
```python
- recipe (ForeignKey → Recipe)     # Target recipe
- user (ForeignKey → User)         # Comment author
- text (TextField)                 # Comment text (max 2000 chars)
- created_at (DateTime)            # Creation timestamp
- updated_at (DateTime)            # Last update timestamp
- likes_count (Integer)            # Number of comment likes
```

**Unique Constraints:** None (users can comment multiple times)

**Ordering:** By `-created_at` (newest first)

---

### 7. Rating Model

**Purpose:** User ratings for recipes (1-5 star system)

**Fields:**
```python
- recipe (ForeignKey → Recipe)     # Target recipe
- user (ForeignKey → User)         # User providing rating
- score (Integer)                  # Rating value (1-5)
- created_at (DateTime)            # Creation timestamp
- updated_at (DateTime)            # Last update timestamp
```

**Unique Constraint:** `(recipe, user)` - One rating per user per recipe

**Validators:** MinValueValidator(1), MaxValueValidator(5)

---

## Views & URL Routing

### Root URL Configuration (`recipe_sharing/urls.py`)

```python
# Main project URL router
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('recipes.urls')),
]
```

### App URL Configuration (`recipes/urls.py`)

```
WEB ROUTES (Traditional HTML responses):
├── GET  /                               → home (home page)
├── GET  /recipe/<id>/                  → recipe_detail (view recipe)
├── GET  /recipe/create/                → create_recipe (new recipe form)
├── POST /recipe/create/                → create_recipe (submit recipe)
├── GET  /recipe/<id>/edit/             → edit_recipe (edit form)
├── POST /recipe/<id>/edit/             → edit_recipe (submit changes)
├── GET  /categories/                   → category_list (all categories)
├── GET  /category/<id>/                → category_detail (category & recipes)
├── GET  /tag/<id>/                     → tag_detail (tag & tagged recipes)
├── GET  /profile/<username>/           → profile (user profile)
├── GET  /profile/edit/                 → edit_profile (edit profile form)
├── POST /profile/edit/                 → edit_profile (submit profile)
└── GET  /register/                     → register (signup form)

API ROUTES (JSON responses via DRF):
├── GET    /api/recipes/                → RecipeViewSet.list()
├── POST   /api/recipes/                → RecipeViewSet.create()
├── GET    /api/recipes/<id>/           → RecipeViewSet.retrieve()
├── PUT    /api/recipes/<id>/           → RecipeViewSet.update()
├── DELETE /api/recipes/<id>/           → RecipeViewSet.destroy()
├── GET    /api/recipes/<id>/comments/  → RecipeViewSet.comments()
├── POST   /api/recipes/<id>/add_comment/ → RecipeViewSet.add_comment()
├── GET    /api/recipes/<id>/ratings/   → RecipeViewSet.ratings()
├── POST   /api/recipes/<id>/add_rating/ → RecipeViewSet.add_rating()
├── GET    /api/categories/             → CategoryViewSet.list()
├── GET    /api/categories/<id>/        → CategoryViewSet.retrieve()
├── GET    /api/categories/<id>/recipes/ → CategoryViewSet.recipes()
├── GET    /api/comments/               → CommentViewSet.list()
└── GET    /api/ratings/                → RatingViewSet.list()
```

### Web Views (`recipes/views.py`)

#### 1. `home(request)` - Homepage
- **Method:** GET
- **Purpose:** Display paginated recipe list with search, filtering, and statistics
- **Template:** `recipes/home.html`
- **Features:**
  - Full-text search across title, description, ingredients, instructions
  - Pagination (6 recipes per page)
  - Category and tag listing
  - Statistics (total recipes, users, categories, tags)
  - Query Parameter: `q` (search query), `page` (page number)

#### 2. `recipe_detail(request, pk)` - Recipe Details
- **Method:** GET, POST
- **Purpose:** Display recipe with comments and ratings
- **Template:** `recipes/recipe_detail.html`
- **Features:**
  - Full recipe information
  - Comments list and form
  - Ratings display and form
  - Average rating calculation
  - Authentication check for comments/ratings
- **POST Actions:**
  - Add comment (requires authentication)
  - Submit rating (requires authentication)

#### 3. `create_recipe(request)` - Create Recipe
- **Method:** GET, POST
- **Purpose:** Recipe creation form
- **Template:** `recipes/create_recipe.html`
- **Requirements:** Login required
- **Features:**
  - Recipe form with all fields
  - File upload for image
  - Category and tags selection
  - Author auto-set to current user

#### 4. `edit_recipe(request, pk)` - Edit Recipe
- **Method:** GET, POST
- **Purpose:** Recipe editing form
- **Template:** `recipes/edit_recipe.html`
- **Requirements:** Login required, author verification
- **Features:**
  - Pre-populated form with recipe data
  - File upload for new image

#### 5. `category_list(request)` - All Categories
- **Method:** GET
- **Purpose:** Display all categories
- **Template:** `recipes/category_list.html`
- **Features:** Category listing with links to detail views

#### 6. `category_detail(request, pk)` - Category Details
- **Method:** GET
- **Purpose:** Display category and its recipes
- **Template:** `recipes/category_detail.html`

#### 7. `tag_detail(request, pk)` - Tag Details
- **Method:** GET
- **Purpose:** Display tag and its recipes
- **Template:** `recipes/tag_detail.html`

#### 8. `profile(request, username)` - User Profile
- **Method:** GET
- **Purpose:** Display user profile and recipes
- **Template:** `recipes/profile.html`
- **Requirements:** Login required
- **Features:**
  - User profile information
  - User's recipes
  - Auto-create profile if needed

#### 9. `edit_profile(request)` - Edit Profile
- **Method:** GET, POST
- **Purpose:** Profile editing form
- **Template:** `recipes/edit_profile.html`
- **Requirements:** Login required
- **Features:**
  - Update bio, avatar, location, website
  - Auto-create profile if needed

#### 10. `register(request)` - User Registration
- **Method:** GET, POST
- **Purpose:** New user signup
- **Template:** `registration/register.html`
- **Features:**
  - Django's UserCreationForm
  - Automatic Profile creation on signup
  - Redirect to login on success

#### 11. `logout_view(request)` - Logout
- **Method:** POST
- **Purpose:** User logout with success message
- **Redirect:** Home page

---

## Templates

### Template Structure

```
templates/
├── base.html                    # Base template with navbar, footer
├── recipes/
│   ├── home.html                # Homepage with recipe grid
│   ├── recipe_detail.html       # Full recipe view with comments/ratings
│   ├── recipe_list.html         # Alternative recipe listing
│   ├── create_recipe.html       # Recipe creation form
│   ├── edit_recipe.html         # Recipe editing form
│   ├── category_list.html       # All categories view
│   ├── category_detail.html     # Category with recipes
│   ├── tag_detail.html          # Tag with recipes
│   ├── profile.html             # User profile view
│   └── edit_profile.html        # Profile editing form
└── registration/
    ├── login.html               # Login form
    ├── logout.html              # Logout confirmation
    └── register.html            # Registration form
```

### Template Context Variables

#### `home.html`
- `recipes` / `page_obj`: Paginated recipe queryset
- `categories`: All categories
- `tags`: All tags
- `recipes_count`: Total recipe count
- `users_count`: Total user count
- `categories_count`: Total category count
- `tags_count`: Total tag count
- `search_query`: Current search term

#### `recipe_detail.html`
- `recipe`: Recipe object
- `comments`: Related comments
- `average_rating`: Calculated average rating
- `comment_form`: CommentForm instance
- `rating_form`: RatingForm instance

#### `profile.html`
- `profile`: Profile object
- `recipes`: User's recipes queryset

---

## API Layer

### REST Framework Configuration

**Router:** DefaultRouter with automatic URL generation

```python
router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe-api')
router.register(r'categories', CategoryViewSet, basename='category-api')
router.register(r'comments', CommentViewSet, basename='comment-api')
router.register(r'ratings', RatingViewSet, basename='rating-api')
```

### ViewSet Implementations

#### CategoryViewSet
**Endpoints:** CRUD operations on categories

**Actions:**
- `GET /api/categories/` - List all
- `POST /api/categories/` - Create (authenticated)
- `GET /api/categories/<id>/` - Retrieve
- `PUT /api/categories/<id>/` - Update (authenticated)
- `DELETE /api/categories/<id>/` - Delete (authenticated)
- **Custom:** `GET /api/categories/<id>/recipes/` - Get category recipes

**Permissions:** `IsAuthenticatedOrReadOnly`

---

#### RecipeViewSet
**Endpoints:** CRUD + custom actions for recipes

**Actions:**
- `GET /api/recipes/` - List (filtered, searchable, orderable)
- `POST /api/recipes/` - Create (authenticated)
- `GET /api/recipes/<id>/` - Retrieve
- `PUT /api/recipes/<id>/` - Update (author only)
- `DELETE /api/recipes/<id>/` - Delete (author only)

**Custom Actions:**
- `GET /api/recipes/<id>/comments/` - Get comments
- `POST /api/recipes/<id>/add_comment/` - Add comment (authenticated)
- `GET /api/recipes/<id>/ratings/` - Get ratings
- `POST /api/recipes/<id>/add_rating/` - Add rating (authenticated)

**Filtering:**
- `category`: Filter by category ID
- `difficulty`: Filter by difficulty level
- `published`: Filter by publication status

**Search Fields:**
- `title`
- `description`
- `ingredients`

**Ordering Fields:**
- `created_at`
- `views_count`
- `likes_count`

**Serializers:**
- List view: `RecipeListSerializer` (lightweight)
- Detail view: `RecipeDetailSerializer` (full data with related objects)

**Permissions:** `IsAuthenticatedOrReadOnly`

---

#### CommentViewSet
**Endpoints:** CRUD operations on comments

**Permissions:** `IsAuthenticatedOrReadOnly`

---

#### RatingViewSet
**Endpoints:** CRUD operations on ratings

**Permissions:** `IsAuthenticatedOrReadOnly`

**Unique Constraint:** One rating per user per recipe

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                         │
│  (Browser / API Client / Mobile App)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
      HTML Requests          API Requests
   (Traditional Forms)      (JSON/REST)
         │                       │
         │                       │
┌────────▼──────────┬───────────▼──────────────────────────┐
│   DJANGO VIEWS    │   DJANGO REST FRAMEWORK VIEWSETS    │
├───────────────────┼──────────────────────────────────────┤
│ • home()          │ • RecipeViewSet                      │
│ • recipe_detail() │ • CategoryViewSet                    │
│ • create_recipe() │ • CommentViewSet                     │
│ • edit_recipe()   │ • RatingViewSet                      │
│ • category_list() │                                      │
│ • profile()       │ Serializers:                         │
│ • edit_profile()  │ • RecipeListSerializer               │
│ • register()      │ • RecipeDetailSerializer             │
│ • logout_view()   │ • CategorySerializer                 │
└────────┬──────────┴─────────────┬──────────────────────┘
         │                        │
         └────────────┬───────────┘
                      │
              Forms & Validation
         (RecipeForm, CommentForm, etc.)
                      │
         ┌────────────▼──────────────┐
         │    DATA MODELS LAYER      │
         ├──────────────────────────┤
         │ • User (Django built-in) │
         │ • Profile                │
         │ • Recipe                 │
         │ • Category               │
         │ • Tag                    │
         │ • Comment                │
         │ • Rating                 │
         └────────────┬──────────────┘
                      │
         ┌────────────▼──────────────┐
         │    DATABASE LAYER        │
         ├──────────────────────────┤
         │ SQLite3 (dev)            │
         │ PostgreSQL (prod ready)  │
         │                          │
         │ db.sqlite3               │
         └──────────────────────────┘

STATIC FILES & TEMPLATES:
┌──────────────┐       ┌──────────────┐
│   Static/    │       │  Templates/  │
├──────────────┤       ├──────────────┤
│ • css/       │       │ • base.html  │
│ • images/    │       │ • recipes/   │
└──────────────┘       │ • register/  │
                       └──────────────┘
```

---

## Request Flow Examples

### Example 1: Creating a Recipe (Web)

```
1. User clicks "Create Recipe" link
2. GET /recipe/create/ → create_recipe view
   - Returns form template: create_recipe.html
   
3. User fills form and submits
4. POST /recipe/create/ → create_recipe view
   - Validates RecipeForm
   - Sets author to current user
   - Saves to database
   - Redirects to recipe_detail page
```

### Example 2: Creating a Recipe (API)

```
1. API Client sends request:
   POST /api/recipes/
   {
     "title": "Pasta Carbonara",
     "description": "...",
     "category": 1,
     "tags": [2, 5],
     ...
   }

2. Request routed to RecipeViewSet.create()
3. RecipeListSerializer validates data
4. perform_create() sets author to request.user
5. Recipe saved to database
6. JSON response returned with created recipe
```

### Example 3: Viewing Recipe with Comments

```
1. GET /recipe/42/
2. recipe_detail view executed
   - Fetches Recipe (pk=42)
   - Fetches related Comments
   - Calculates average Rating
   - Renders template with context
3. Response: HTML page with full recipe display
```

---

## Authentication & Authorization

### Built-in Django Auth
- User registration via `register()` view
- Login/Logout via Django contrib auth
- Profile auto-creation on signup

### Permission Classes (API)
- `IsAuthenticatedOrReadOnly`: Read for everyone, write for authenticated users
- `IsAuthenticated`: Only authenticated users can access

### View-Level Authorization
- `@login_required` decorator on protected views
- Owner verification (e.g., recipe author can only edit own recipes)

---

## Database Relationships Summary

```
User (Django Auth)
├─ 1:N → Recipe (author)
├─ 1:N → Comment (user)
├─ 1:N → Rating (user)
└─ 1:1 → Profile (user)

Profile
└─ 1:1 → User

Category
└─ 1:N → Recipe

Recipe
├─ N:1 → User (author)
├─ N:1 → Category
├─ N:N → Tag
├─ 1:N → Comment
└─ 1:N → Rating

Comment
├─ N:1 → Recipe
└─ N:1 → User

Rating
├─ N:1 → Recipe
└─ N:1 → User

Tag
└─ N:N → Recipe
```

---

## Configuration Highlights

### Settings (`recipe_sharing/settings.py`)

**Key Settings:**
- `DEBUG`: Environment variable (development/production)
- `SECRET_KEY`: Environment variable for security
- `ALLOWED_HOSTS`: Localhost, 127.0.0.1, Render.com hosts
- `DATABASES`: SQLite (dev) or PostgreSQL (production)
- `STATIC_ROOT`: WhiteNoise for production static file serving
- `MEDIA_ROOT`: User uploads in `/media/` directory
- `LOGIN_REDIRECT_URL`: Redirects to home after login
- `LOGOUT_REDIRECT_URL`: Redirects to home after logout

**Middleware Stack:**
1. SecurityMiddleware
2. WhiteNoiseMiddleware (if available)
3. SessionMiddleware
4. CommonMiddleware
5. CsrfViewMiddleware
6. AuthenticationMiddleware
7. MessageMiddleware
8. XFrameOptionsMiddleware

---

## Summary

This Django project implements a **Recipe Sharing Platform** with:

✅ **Traditional Web Interface** - Server-side rendered HTML templates  
✅ **RESTful API** - JSON endpoints for mobile/frontend clients  
✅ **Django ORM** - Well-structured relational data models  
✅ **Authentication** - Built-in Django user system with extended profiles  
✅ **Content Management** - Create, read, update recipes with images  
✅ **Social Features** - Comments, ratings, user profiles  
✅ **Search & Filtering** - Full-text search and category filtering  
✅ **Production Ready** - WhiteNoise, environment-based configuration, PostgreSQL support

---

# 6. Implementation Details

## Key Models Implementation

### Recipe Model - Core Implementation

```python
class Recipe(models.Model):
    # Owner & Metadata
    author = ForeignKey(User, on_delete=CASCADE, related_name='recipes')
    
    # Content Fields
    title = CharField(max_length=200)
    description = TextField(max_length=1000)
    ingredients = TextField()  # Newline-separated
    instructions = TextField()
    image = ImageField(upload_to='recipes/')
    
    # Organization
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)
    tags = ManyToManyField(Tag, blank=True)
    
    # Recipe Details
    prep_time = IntegerField()  # minutes
    cook_time = IntegerField()  # minutes
    servings = IntegerField(validators=[MinValueValidator(1)])
    difficulty = CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    
    # Engagement Metrics
    views_count = IntegerField(default=0)
    likes_count = IntegerField(default=0)
    
    # Publishing & Timestamps
    published = BooleanField(default=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    # Methods
    def get_total_time(self):
        return (self.prep_time or 0) + (self.cook_time or 0)
    
    def get_average_rating(self):
        ratings = self.ratings.all()
        return sum(r.score for r in ratings) / len(ratings) if ratings else 0
```

**Key Design Decisions:**
- `author` via ForeignKey ensures data consistency (cascade delete)
- `tags` ManyToMany allows flexible categorization
- `published` boolean supports draft recipes
- Computed methods (`get_total_time`, `get_average_rating`) avoid storing derived data

---

### Profile Model - Authentication Extension

```python
class Profile(models.Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='profile')
    bio = TextField(blank=True, max_length=500)
    avatar = ImageField(upload_to='avatars/', blank=True, null=True)
    location = CharField(max_length=100, blank=True)
    website = URLField(blank=True, null=True)
    followers_count = IntegerField(default=0)  # Denormalized for performance
    following_count = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
```

**Design Rationale:**
- OneToOne relationship allows optional profile data
- Auto-created during user registration
- Social counters denormalized for quick access

---

### Comment & Rating Models - Engagement

```python
class Comment(models.Model):
    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name='comments')
    user = ForeignKey(User, on_delete=CASCADE, related_name='recipe_comments')
    text = TextField(max_length=2000)
    created_at = DateTimeField(auto_now_add=True)
    
class Rating(models.Model):
    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name='ratings')
    user = ForeignKey(User, on_delete=CASCADE, related_name='recipe_ratings')
    score = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    class Meta:
        unique_together = ('recipe', 'user')  # One rating per user
```

**Design Rationale:**
- Comments allow discussion without unique constraint
- Ratings have `unique_together` to prevent duplicate votes
- Both cascade delete with recipe for data integrity

---

## Forms Implementation

### RecipeForm - Content Creation

```python
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 
                  'category', 'tags', 'image']
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'ingredients': Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'instructions': Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-select'}),
            'tags': SelectMultiple(attrs={'class': 'form-select'}),
            'image': FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
```

**Features:**
- Bootstrap CSS classes for styling
- HTML5 input attributes (`accept='image/*'`)
- TextArea for long-form content with predefined rows

### CommentForm & RatingForm

```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # User and recipe auto-set in view

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']  # User and recipe auto-set in view
```

**Pattern:** User and relationship fields set in views, not exposed in forms

---

## Views Logic

### Homepage View - Search & Pagination

```python
def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    
    # Full-text search
    search_query = request.GET.get('q', '').strip()
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query) |
            Q(instructions__icontains=search_query)
        )
    
    # Pagination (6 per page)
    paginator = Paginator(recipes, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    # Statistics
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'recipes_count': Recipe.objects.count(),
        'search_query': search_query,
    }
    return render(request, 'recipes/home.html', context)
```

**Logic Patterns:**
- Q objects for OR queries
- icontains for case-insensitive search
- Paginator for performance on large datasets
- Database count aggregation

---

### Recipe Detail View - Form Handling

```python
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        form_type = request.POST.get('form_type')
        
        if form_type == 'comment':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added!')
                return redirect('recipe_detail', pk=pk)
                
        elif form_type == 'rating':
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating, created = Rating.objects.get_or_create(
                    recipe=recipe,
                    user=request.user,
                    defaults={'score': rating_form.cleaned_data['score']}
                )
                if not created:
                    rating.score = rating_form.cleaned_data['score']
                    rating.save()
    
    # GET: Display forms
    average_rating = recipe.ratings.aggregate(Avg('score'))['score__avg'] or 0
    context = {
        'recipe': recipe,
        'comments': recipe.comments.all(),
        'average_rating': average_rating,
        'comment_form': CommentForm(),
        'rating_form': RatingForm(),
    }
    return render(request, 'recipes/recipe_detail.html', context)
```

**Logic Patterns:**
- `get_or_create()` for update-or-create ratings
- `commit=False` to add fields before saving
- Multiple form handling with form_type flag
- Authentication checks
- Messages framework for user feedback
- Aggregate functions for calculations

---

### Recipe Create/Edit Views - CRUD Operations

```python
@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Set current user
            recipe.save()
            form.save_m2m()  # Save ManyToMany relationships
            messages.success(request, 'Recipe created!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    # Author verification in query
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()  # Saves all including M2M
            messages.success(request, 'Recipe updated!')
            return redirect('recipe_detail', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form})
```

**Security Patterns:**
- `@login_required` decorator prevents unauthenticated access
- `author=request.user` in query prevents unauthorized edits
- `request.FILES` handles file uploads

---

## API Serializers

### RecipeDetailSerializer - Full Data

```python
class RecipeDetailSerializer(serializers.ModelSerializer):
    # Read-only nested serializers
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    # Write-only PK fields
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True
    )
    
    # Computed fields
    average_rating = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()
```

**Design Patterns:**
- Separate read/write serialization for relationships
- `SerializerMethodField` for computed data
- Nested serializers for related data
- Read-only timestamps

---

### RecipeListSerializer - Lightweight Version

```python
class RecipeListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        fields = ['id', 'title', 'author_username', 'category_name', 
                  'difficulty', 'views_count', 'average_rating', 'created_at']
```

**Optimization:** Reduces payload by excluding large fields like `ingredients` and `instructions`

---

## ViewSet Implementations

### RecipeViewSet - Custom Actions

```python
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.filter(published=True).order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filtering, searching, ordering
    filterset_fields = ['category', 'difficulty', 'published']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'views_count', 'likes_count']
    
    # Dynamic serializer selection
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return RecipeListSerializer
    
    # Authorization enforcement
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        recipe = self.get_object()
        if recipe.author != self.request.user:
            raise PermissionDenied("Only the author can edit this recipe")
        serializer.save()
    
    # Custom actions
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        recipe = self.get_object()
        text = request.data.get('text')
        
        if not text:
            return Response({'detail': 'Text required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment.objects.create(
            user=request.user,
            recipe=recipe,
            text=text
        )
        return Response(CommentSerializer(comment).data, 
                       status=status.HTTP_201_CREATED)
```

**Patterns:**
- `filterset_fields` for database-level filtering
- `search_fields` with full-text search
- `get_serializer_class()` for conditional serialization
- Custom actions with decorators
- Permission checks in `perform_*` methods

---

# 7. Challenges & Solutions

## Challenge 1: User Authorization in APIs

**Problem:** How to ensure users can only edit their own recipes/comments?

**Solution:**
```python
# In ViewSet
def perform_update(self, serializer):
    obj = self.get_object()
    if obj.user != self.request.user and obj.author != self.request.user:
        raise PermissionDenied("Not authorized")
    serializer.save()

# Alternative: Use custom permissions
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.author == request.user
```

---

## Challenge 2: Profile Auto-Creation

**Problem:** Profile must exist when accessing user profile view, but needs to be created on signup.

**Solution:**
```python
# In registration view
def register(request):
    if form.is_valid():
        user = form.save()
        Profile.objects.create(user=user)  # Auto-create
        return redirect('login')

# In profile view
profile, created = Profile.objects.get_or_create(user=user)
# Ensures profile exists even if created before auto-creation existed
```

---

## Challenge 3: One Rating Per User Per Recipe

**Problem:** Users should only have one rating per recipe, but allow updates.

**Solution:**
```python
class Rating(models.Model):
    class Meta:
        unique_together = ('recipe', 'user')  # Database constraint

# In view using get_or_create
def add_rating(self, request, pk=None):
    recipe = self.get_object()
    rating, created = Rating.objects.update_or_create(
        user=request.user,
        recipe=recipe,
        defaults={'score': request.data['score']}
    )
    return Response(RatingSerializer(rating).data)
```

---

## Challenge 4: Search Performance

**Problem:** Full-text search across multiple fields can be slow.

**Solution:**
```python
# Initial solution: ORM Q objects
recipes = Recipe.objects.filter(
    Q(title__icontains=query) |
    Q(description__icontains=query) |
    Q(ingredients__icontains=query)
)

# Optimization: Database indexing
class Recipe(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]

# Advanced: Could use PostgreSQL full-text search (django-search)
```

---

## Challenge 5: ManyToMany with ModelForm

**Problem:** Saving ManyToMany fields requires special handling.

**Solution:**
```python
# In create view
form = RecipeForm(request.POST, request.FILES)
if form.is_valid():
    recipe = form.save(commit=False)  # Don't save yet
    recipe.author = request.user
    recipe.save()  # Save main object
    form.save_m2m()  # Then save M2M relationships

# In edit view
form = RecipeForm(request.POST, request.FILES, instance=recipe)
if form.is_valid():
    form.save()  # Handles M2M automatically
```

---

## Challenge 6: API Serializer Read/Write Differences

**Problem:** API needs to accept `category_id` (write) but return full `category` object (read).

**Solution:**
```python
class RecipeDetailSerializer(serializers.ModelSerializer):
    # For responses (read-only nested object)
    category = CategorySerializer(read_only=True)
    
    # For requests (write-only PK)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
```

---

## Challenge 7: Image Upload Handling

**Problem:** Need to handle image uploads in forms and validate file types.

**Solution:**
```python
class RecipeForm(forms.ModelForm):
    widgets = {
        'image': forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'  # HTML5 attribute
        }),
    }

# In settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# In urls.py (development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                         document_root=settings.MEDIA_ROOT)
```

---

## Challenge 8: Pagination with Search

**Problem:** Pagination must work while maintaining search filters.

**Solution:**
```python
def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('q', '').strip()
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(recipes, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,  # Pass back to template
    }
    return render(request, 'home.html', context)

# In template
<a href="?q={{ search_query }}&page={{ page_obj.next_page_number }}">Next</a>
```

---

# 8. Conclusion

## What Was Learned

### 1. **Django Architecture**
- Separation of concerns: Models → Views → Templates
- Importance of `commit=False` in form handling
- ViewSets reduce boilerplate significantly

### 2. **Authorization & Security**
- Always verify ownership before allowing updates
- Use permission classes consistently
- Leverage `@login_required` and query-level filters

### 3. **ORM Best Practices**
- Use `select_related()` and `prefetch_related()` to prevent N+1 queries
- Leverage `unique_together` for database-level constraints
- Computed fields should use methods, not stored data

### 4. **API Design**
- Different serializers for list vs. detail views
- Nested relationships improve DX
- Custom actions are powerful for complex operations

### 5. **Form Handling**
- Separate read/write fields in serializers
- Use widgets for validation and UX
- Handle ManyToMany explicitly

### 6. **Deployment Considerations**
- Environment variables for sensitive data
- WhiteNoise for static file serving
- Support multiple database backends

---

## Possible Future Improvements

**Short-term (Quick wins):**
- Add recipe image optimization (resize, compression)
- Implement recipe soft-delete (add `is_deleted` flag)
- Add recipe favorites/bookmarks with M2M model
- Implement pagination filters in API

**Medium-term (1-2 weeks):**
- Add advanced search with Elasticsearch
- Implement user follow system with notifications
- Add recipe versioning/history tracking
- Create recipe recommendation algorithm
- Add ingredient inventory tracking

**Long-term (Strategic):**
- Implement GraphQL API for flexible queries
- Add real-time collaboration features (WebSockets)
- Machine learning for recipe suggestions
- Social feed with activity notifications
- Meal plan generation from recipes
- Nutrition calculation integration

**Performance Optimizations:**
- Redis caching for frequently accessed recipes
- Database query optimization with select/prefetch
- CDN for image delivery
- API rate limiting and throttling
- Async tasks for image processing (Celery)

**Code Quality:**
- Add comprehensive unit tests (80%+ coverage)
- Implement continuous integration/deployment
- Add type hints throughout codebase
- API versioning (v1, v2 endpoints)
- Swagger/OpenAPI documentation

---

**Project Status:** ✅ **Feature Complete & Production-Ready**  
**Performance:** ✅ **Optimized with indexing and pagination**  
**Security:** ✅ **Authorization checks, CSRF protection**  
**Scalability:** ✅ **Ready for PostgreSQL and cloud deployment**
