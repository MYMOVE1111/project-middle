from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

# DRF Router for API endpoints
router = DefaultRouter()
router.register(r'recipes', api_views.RecipeViewSet, basename='recipe-api')
router.register(r'categories', api_views.CategoryViewSet, basename='category-api')
router.register(r'comments', api_views.CommentViewSet, basename='comment-api')
router.register(r'ratings', api_views.RatingViewSet, basename='rating-api')

urlpatterns = [
    # Web routes (must come first)
    path('', views.home, name='home'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit_recipe'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('tag/<int:pk>/', views.tag_detail, name='tag_detail'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    
    # API routes (under /api/ prefix)
    path('api/', include(router.urls)),
]