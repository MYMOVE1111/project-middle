from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# ============================================================
# CATEGORY MODEL
# ============================================================
class Category(models.Model):
    """
    Represents recipe categories (e.g., Breakfast, Dessert, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# ============================================================
# TAG MODEL
# ============================================================
class Tag(models.Model):
    """
    Represents tags for recipes (e.g., Vegan, Gluten-Free, etc.)
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ============================================================
# USER PROFILE MODEL
# ============================================================
class Profile(models.Model):
    """
    Extended user profile with additional information
    One-to-One relationship with Django's User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True, null=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ============================================================
# RECIPE MODEL (Core Model)
# ============================================================
class Recipe(models.Model):
    """
    Main Recipe model with comprehensive details
    - Authored by User (ForeignKey)
    - Belongs to Category (ForeignKey)
    - Can have multiple Tags (ManyToMany)
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    ingredients = models.TextField(help_text="Separate each ingredient with a new line")
    instructions = models.TextField(help_text="Detailed cooking instructions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='recipes')
    tags = models.ManyToManyField(Tag, blank=True, related_name='recipes')
    
    # Additional Recipe Details
    prep_time = models.IntegerField(help_text="Preparation time in minutes", null=True, blank=True)
    cook_time = models.IntegerField(help_text="Cooking time in minutes", null=True, blank=True)
    servings = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    
    # Engagement Metrics
    views_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_total_time(self):
        """Calculate total cooking time"""
        if self.prep_time and self.cook_time:
            return self.prep_time + self.cook_time
        return self.prep_time or self.cook_time or 0

    def get_average_rating(self):
        """Calculate average rating for the recipe"""
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(r.score for r in ratings) / ratings.count()
        return 0


# ============================================================
# COMMENT MODEL
# ============================================================
class Comment(models.Model):
    """
    User comments on recipes
    - Linked to Recipe (ForeignKey)
    - Authored by User (ForeignKey)
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_comments')
    text = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    likes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipe', '-created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"


# ============================================================
# RATING MODEL
# ============================================================
class Rating(models.Model):
    """
    User ratings for recipes (1-5 stars)
    - Linked to Recipe (ForeignKey)
    - Authored by User (ForeignKey)
    - Unique constraint: One rating per user per recipe
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_ratings')
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('recipe', 'user')
        indexes = [
            models.Index(fields=['recipe', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.title}: {self.score}/5"