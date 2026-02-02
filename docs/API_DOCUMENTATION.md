# Django REST API Documentation

## Overview

The Recipe Sharing application includes a comprehensive REST API built with **Django REST Framework (DRF)** supporting full CRUD operations for recipes, categories, comments, and ratings.

**Base URL**: `http://localhost:8000/`

---

## 🔐 Authentication

### Session Authentication
- Use Django's session-based authentication (login via web interface)
- Session cookie automatically sent with requests from the same browser

### Permissions
- **Public Users**: Can GET (read) all published recipes and categories
- **Authenticated Users**: Can POST (create), PUT (update), DELETE own content
- **Content Authors**: Can edit/delete only their own content

---

## 📋 API Endpoints

### 1. Recipes API

#### 1.1 GET - List All Recipes
```
GET /api/recipes/
```

**Description**: Retrieve a paginated list of all published recipes.

**Query Parameters**:
- `page` (int): Page number for pagination (default: 1)
- `category` (int): Filter by category ID
- `difficulty` (str): Filter by difficulty (easy, medium, hard)
- `search` (str): Search by title, description, or ingredients
- `ordering` (str): Sort by created_at, views_count, likes_count

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/recipes/?page=1&category=1&difficulty=easy"
```

**Response** (200 OK):
```json
{
    "count": 13,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Classic Pasta Carbonara",
            "author": 1,
            "author_username": "admin",
            "category": 1,
            "category_name": "Italian",
            "prep_time": 10,
            "cook_time": 20,
            "servings": 4,
            "difficulty": "easy",
            "published": true,
            "views_count": 125,
            "likes_count": 34,
            "average_rating": 4.5,
            "image": "/media/recipes/pasta.jpg",
            "created_at": "2025-10-15T10:30:00Z"
        },
        {
            "id": 2,
            "title": "Greek Salad",
            "author": 2,
            "author_username": "user1",
            "category": 2,
            "category_name": "Salads",
            "prep_time": 15,
            "cook_time": 0,
            "servings": 2,
            "difficulty": "easy",
            "published": true,
            "views_count": 89,
            "likes_count": 21,
            "average_rating": 4.2,
            "image": "/media/recipes/salad.jpg",
            "created_at": "2025-10-14T14:20:00Z"
        }
    ]
}
```

---

#### 1.2 POST - Create a New Recipe
```
POST /api/recipes/
```

**Description**: Create a new recipe (requires authentication).

**Authentication**: Required (login first)

**Request Body**:
```json
{
    "title": "Homemade Pizza",
    "description": "Delicious homemade pizza with fresh ingredients",
    "ingredients": "Flour, Tomato sauce, Mozzarella cheese, Basil, Olive oil",
    "instructions": "1. Make dough\n2. Add sauce\n3. Add toppings\n4. Bake at 400F for 20 minutes",
    "category_id": 1,
    "tag_ids": [1, 3],
    "prep_time": 30,
    "cook_time": 20,
    "servings": 4,
    "difficulty": "medium",
    "published": true
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/recipes/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Homemade Pizza",
    "description": "Delicious homemade pizza",
    "ingredients": "Flour, Tomato sauce, Mozzarella cheese",
    "instructions": "1. Make dough 2. Add sauce 3. Bake",
    "category_id": 1,
    "prep_time": 30,
    "cook_time": 20,
    "servings": 4,
    "difficulty": "medium",
    "published": true
  }'
```

**Response** (201 Created):
```json
{
    "id": 14,
    "title": "Homemade Pizza",
    "description": "Delicious homemade pizza with fresh ingredients",
    "ingredients": "Flour, Tomato sauce, Mozzarella cheese, Basil, Olive oil",
    "instructions": "1. Make dough\n2. Add sauce\n3. Add toppings\n4. Bake at 400F for 20 minutes",
    "author": 1,
    "author_username": "admin",
    "category": 1,
    "category_id": 1,
    "tags": [],
    "tag_ids": [1, 3],
    "prep_time": 30,
    "cook_time": 20,
    "servings": 4,
    "difficulty": "medium",
    "published": true,
    "created_at": "2025-10-20T12:00:00Z",
    "updated_at": "2025-10-20T12:00:00Z",
    "views_count": 0,
    "likes_count": 0,
    "average_rating": 0,
    "comments_count": 0,
    "image": null
}
```

---

#### 1.3 GET - Retrieve Recipe Detail
```
GET /api/recipes/{id}/
```

**Description**: Get detailed information about a specific recipe.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/recipes/1/"
```

**Response** (200 OK):
```json
{
    "id": 1,
    "title": "Classic Pasta Carbonara",
    "description": "Traditional Italian pasta with creamy sauce",
    "ingredients": "400g pasta, 200g bacon, 4 eggs, 100g Parmesan cheese, Salt, Black pepper",
    "instructions": "1. Cook pasta\n2. Fry bacon\n3. Mix eggs and cheese\n4. Combine all",
    "author": 1,
    "author_username": "admin",
    "category": {
        "id": 1,
        "name": "Italian",
        "description": "Italian cuisine",
        "created_at": "2025-10-01T00:00:00Z"
    },
    "category_id": 1,
    "tags": [
        {
            "id": 1,
            "name": "pasta",
            "created_at": "2025-10-01T00:00:00Z"
        }
    ],
    "tag_ids": [1],
    "prep_time": 10,
    "cook_time": 20,
    "servings": 4,
    "difficulty": "easy",
    "published": true,
    "created_at": "2025-10-15T10:30:00Z",
    "updated_at": "2025-10-15T10:30:00Z",
    "views_count": 125,
    "likes_count": 34,
    "average_rating": 4.5,
    "comments_count": 3,
    "image": "/media/recipes/pasta.jpg"
}
```

---

#### 1.4 PUT - Update Recipe
```
PUT /api/recipes/{id}/
```

**Description**: Update a recipe (only author can update).

**Authentication**: Required

**Example Request**:
```bash
curl -X PUT "http://localhost:8000/api/recipes/1/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Pasta Carbonara",
    "description": "Updated description"
  }'
```

**Response** (200 OK): Updated recipe object

---

#### 1.5 DELETE - Delete Recipe
```
DELETE /api/recipes/{id}/
```

**Description**: Delete a recipe (only author can delete).

**Authentication**: Required

**Example Request**:
```bash
curl -X DELETE "http://localhost:8000/api/recipes/1/"
```

**Response** (204 No Content)

---

#### 1.6 GET - Recipe Comments
```
GET /api/recipes/{id}/comments/
```

**Description**: Get all comments for a recipe.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/recipes/1/comments/"
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "user": 2,
        "user_username": "user1",
        "recipe": 1,
        "recipe_title": "Classic Pasta Carbonara",
        "text": "Great recipe! Very easy to follow.",
        "created_at": "2025-10-16T14:30:00Z",
        "updated_at": "2025-10-16T14:30:00Z",
        "likes_count": 2
    }
]
```

---

#### 1.7 POST - Add Comment to Recipe
```
POST /api/recipes/{id}/add_comment/
```

**Description**: Add a comment to a recipe (requires authentication).

**Authentication**: Required

**Request Body**:
```json
{
    "text": "This recipe is amazing! I made it for dinner."
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/recipes/1/add_comment/" \
  -H "Content-Type: application/json" \
  -d '{"text": "This recipe is amazing!"}'
```

**Response** (201 Created):
```json
{
    "id": 5,
    "user": 2,
    "user_username": "user1",
    "recipe": 1,
    "recipe_title": "Classic Pasta Carbonara",
    "text": "This recipe is amazing! I made it for dinner.",
    "created_at": "2025-10-20T12:00:00Z",
    "updated_at": "2025-10-20T12:00:00Z",
    "likes_count": 0
}
```

---

#### 1.8 GET - Recipe Ratings
```
GET /api/recipes/{id}/ratings/
```

**Description**: Get all ratings for a recipe.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/recipes/1/ratings/"
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "user": 2,
        "user_username": "user1",
        "recipe": 1,
        "recipe_title": "Classic Pasta Carbonara",
        "score": 5,
        "created_at": "2025-10-16T15:00:00Z"
    },
    {
        "id": 2,
        "user": 3,
        "user_username": "user2",
        "recipe": 1,
        "recipe_title": "Classic Pasta Carbonara",
        "score": 4,
        "created_at": "2025-10-17T10:00:00Z"
    }
]
```

---

#### 1.9 POST - Add/Update Rating for Recipe
```
POST /api/recipes/{id}/add_rating/
```

**Description**: Add or update a rating for a recipe (requires authentication).

**Authentication**: Required

**Request Body**:
```json
{
    "score": 5
}
```

**Constraints**: Score must be between 1 and 5

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/recipes/1/add_rating/" \
  -H "Content-Type: application/json" \
  -d '{"score": 5}'
```

**Response** (201 Created - if new, 200 OK - if updated):
```json
{
    "id": 1,
    "user": 2,
    "user_username": "user1",
    "recipe": 1,
    "recipe_title": "Classic Pasta Carbonara",
    "score": 5,
    "created_at": "2025-10-20T12:00:00Z"
}
```

---

#### 1.10 GET - Recipe Average Rating
```
GET /api/recipes/{id}/average_rating/
```

**Description**: Get the average rating for a recipe.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/recipes/1/average_rating/"
```

**Response** (200 OK):
```json
{
    "id": 1,
    "title": "Classic Pasta Carbonara",
    "average_rating": 4.5,
    "total_ratings": 6
}
```

---

### 2. Categories API

#### 2.1 GET - List All Categories
```
GET /api/categories/
```

**Description**: Retrieve all recipe categories.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/categories/"
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "name": "Italian",
        "description": "Italian cuisine",
        "created_at": "2025-10-01T00:00:00Z"
    },
    {
        "id": 2,
        "name": "Salads",
        "description": "Healthy salad recipes",
        "created_at": "2025-10-01T00:00:00Z"
    }
]
```

---

#### 2.2 POST - Create Category
```
POST /api/categories/
```

**Description**: Create a new category (requires authentication).

**Authentication**: Required

**Request Body**:
```json
{
    "name": "Desserts",
    "description": "Sweet dessert recipes"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Desserts", "description": "Sweet dessert recipes"}'
```

**Response** (201 Created):
```json
{
    "id": 6,
    "name": "Desserts",
    "description": "Sweet dessert recipes",
    "created_at": "2025-10-20T12:00:00Z"
}
```

---

#### 2.3 GET - Retrieve Category Detail
```
GET /api/categories/{id}/
```

**Description**: Get details of a specific category.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/categories/1/"
```

**Response** (200 OK):
```json
{
    "id": 1,
    "name": "Italian",
    "description": "Italian cuisine",
    "created_at": "2025-10-01T00:00:00Z"
}
```

---

#### 2.4 GET - Category Recipes
```
GET /api/categories/{id}/recipes/
```

**Description**: Get all recipes in a category.

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/categories/1/recipes/"
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "title": "Classic Pasta Carbonara",
        "author": 1,
        "author_username": "admin",
        "category": 1,
        "category_name": "Italian",
        "prep_time": 10,
        "cook_time": 20,
        "servings": 4,
        "difficulty": "easy",
        "published": true,
        "views_count": 125,
        "likes_count": 34,
        "average_rating": 4.5,
        "image": "/media/recipes/pasta.jpg",
        "created_at": "2025-10-15T10:30:00Z"
    }
]
```

---

### 3. Comments API

#### 3.1 GET - List All Comments
```
GET /api/comments/
```

**Description**: Retrieve all comments (paginated).

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/comments/"
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "user": 2,
        "user_username": "user1",
        "recipe": 1,
        "recipe_title": "Classic Pasta Carbonara",
        "text": "Great recipe! Very easy to follow.",
        "created_at": "2025-10-16T14:30:00Z",
        "updated_at": "2025-10-16T14:30:00Z",
        "likes_count": 2
    }
]
```

---

#### 3.2 POST - Create Comment
```
POST /api/comments/
```

**Description**: Create a new comment (requires authentication).

**Authentication**: Required

**Request Body**:
```json
{
    "recipe": 1,
    "text": "Excellent recipe! Made it for my family."
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/comments/" \
  -H "Content-Type: application/json" \
  -d '{"recipe": 1, "text": "Excellent recipe!"}'
```

**Response** (201 Created):
```json
{
    "id": 2,
    "user": 2,
    "user_username": "user1",
    "recipe": 1,
    "recipe_title": "Classic Pasta Carbonara",
    "text": "Excellent recipe! Made it for my family.",
    "created_at": "2025-10-20T12:00:00Z",
    "updated_at": "2025-10-20T12:00:00Z",
    "likes_count": 0
}
```

---

### 4. Ratings API

#### 4.1 GET - List All Ratings
```
GET /api/ratings/
```

**Description**: Retrieve all ratings (paginated).

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/ratings/"
```

**Response** (200 OK):
```json
[
    {
        "id": 1,
        "user": 2,
        "user_username": "user1",
        "recipe": 1,
        "recipe_title": "Classic Pasta Carbonara",
        "score": 5,
        "created_at": "2025-10-16T15:00:00Z"
    }
]
```

---

#### 4.2 POST - Create Rating
```
POST /api/ratings/
```

**Description**: Create a new rating (requires authentication).

**Authentication**: Required

**Request Body**:
```json
{
    "recipe": 1,
    "score": 4
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/ratings/" \
  -H "Content-Type: application/json" \
  -d '{"recipe": 1, "score": 4}'
```

**Response** (201 Created):
```json
{
    "id": 6,
    "user": 2,
    "user_username": "user1",
    "recipe": 1,
    "recipe_title": "Classic Pasta Carbonara",
    "score": 4,
    "created_at": "2025-10-20T12:00:00Z"
}
```

---

## ⚙️ Query Parameters

### Pagination
```
?page=1
```
Default page size: 10 items per page

### Filtering (Recipes)
```
?category=1           # Filter by category ID
?difficulty=easy      # Filter by difficulty (easy, medium, hard)
?published=true       # Filter by published status
```

### Search (Recipes)
```
?search=pasta         # Search in title, description, ingredients
```

### Ordering (Recipes)
```
?ordering=created_at     # Order by creation date (ascending)
?ordering=-created_at    # Order by creation date (descending)
?ordering=views_count    # Order by views
?ordering=likes_count    # Order by likes
```

---

## 🔑 Error Responses

### 400 Bad Request
```json
{
    "detail": "Invalid request data",
    "field_name": ["This field is required."]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "Only the recipe author can update this recipe."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```

---

## 📝 HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

---

## 🧪 Testing with cURL

### Step 1: Login (Get Session Cookie)
```bash
curl -X POST "http://localhost:8000/accounts/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=your_password" \
  -c cookies.txt
```

### Step 2: Make API Requests (Using Session)
```bash
curl -X GET "http://localhost:8000/api/recipes/" \
  -b cookies.txt
```

### Step 3: Create Recipe (With Authentication)
```bash
curl -X POST "http://localhost:8000/api/recipes/" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "My Recipe",
    "description": "Recipe description",
    "ingredients": "ingredient1, ingredient2",
    "instructions": "step 1, step 2",
    "category_id": 1,
    "prep_time": 30,
    "cook_time": 20,
    "servings": 4,
    "difficulty": "easy",
    "published": true
  }'
```

---

## 🧪 Testing with Postman

### 1. Import Collection
- Open Postman
- Click "Import"
- Choose the included Postman collection file

### 2. Set Environment Variables
```
{{base_url}} = http://localhost:8000
{{username}} = admin
{{password}} = your_password
```

### 3. Run Requests
- Use pre-built request templates
- Requests automatically handle authentication
- View responses in JSON format

### 4. Create Request from Scratch

**Example: GET Recipes**
1. Method: GET
2. URL: `{{base_url}}/api/recipes/`
3. Headers:
   - `Content-Type: application/json`
4. Click "Send"

**Example: POST Recipe**
1. Method: POST
2. URL: `{{base_url}}/api/recipes/`
3. Headers:
   - `Content-Type: application/json`
4. Body (JSON):
   ```json
   {
       "title": "New Recipe",
       "description": "Description",
       "ingredients": "ingredient1, ingredient2",
       "instructions": "step1, step2",
       "category_id": 1,
       "prep_time": 30,
       "cook_time": 20,
       "servings": 4,
       "difficulty": "easy",
       "published": true
   }
   ```
5. Click "Send"

---

## 📊 API Statistics

| Component | Count |
|-----------|-------|
| ViewSets | 4 |
| Serializers | 6 |
| API Endpoints | 15+ |
| Custom Actions | 5 |
| Supported Operations | GET, POST, PUT, DELETE |

---

## ✅ API Features

✅ Full CRUD operations
✅ Authentication & Permissions
✅ Pagination support
✅ Search & filtering
✅ Custom actions (add_comment, add_rating)
✅ Browsable API
✅ Comprehensive error handling
✅ Request validation
✅ Serialization/Deserialization
✅ Related data inclusion

---

## 🚀 Production Deployment Notes

Before deploying to production:

1. **Security**:
   - Set `DEBUG = False`
   - Use proper authentication (Token, JWT)
   - Implement rate limiting
   - Add CORS headers

2. **Performance**:
   - Enable caching
   - Optimize queries (select_related, prefetch_related)
   - Add database indexes
   - Use pagination

3. **Documentation**:
   - Use Swagger/OpenAPI for auto-docs
   - Implement API versioning
   - Add request/response examples

4. **Testing**:
   - Write unit tests
   - Integration tests
   - Load testing
   - Security testing

