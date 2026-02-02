from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Profile, Recipe, Comment, Rating


# ============================================================
# CATEGORY ADMIN
# ============================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model
    """
    list_display = ['name', 'recipe_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def recipe_count(self, obj):
        """Display number of recipes in category"""
        count = obj.recipes.count()
        return format_html(
            '<span style="background-color: #417690; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    recipe_count.short_description = 'Recipes'


# ============================================================
# TAG ADMIN
# ============================================================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin interface for Tag model
    """
    list_display = ['name', 'recipe_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Tag Information', {
            'fields': ('name',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def recipe_count(self, obj):
        """Display number of recipes with this tag"""
        count = obj.recipes.count()
        return format_html(
            '<span style="background-color: #79aec8; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    recipe_count.short_description = 'Recipes'


# ============================================================
# PROFILE ADMIN
# ============================================================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for Profile model
    """
    list_display = ['user', 'location', 'followers_display', 'following_display', 'created_at']
    search_fields = ['user__username', 'user__email', 'location', 'bio']
    list_filter = ['created_at', 'followers_count', 'following_count']
    readonly_fields = ['user', 'created_at', 'updated_at', 'avatar_preview']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar', 'avatar_preview')
        }),
        ('Profile Details', {
            'fields': ('bio', 'location', 'website')
        }),
        ('Social Stats', {
            'fields': ('followers_count', 'following_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def followers_display(self, obj):
        """Display followers count with styling"""
        return format_html(
            '<span style="background-color: #70bf2b; color: white; padding: 3px 8px; border-radius: 3px;">👥 {}</span>',
            obj.followers_count
        )
    followers_display.short_description = 'Followers'
    
    def following_display(self, obj):
        """Display following count with styling"""
        return format_html(
            '<span style="background-color: #ef8537; color: white; padding: 3px 8px; border-radius: 3px;">🔗 {}</span>',
            obj.following_count
        )
    following_display.short_description = 'Following'
    
    def avatar_preview(self, obj):
        """Show image preview"""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return 'No avatar'
    avatar_preview.short_description = 'Avatar Preview'


# ============================================================
# COMMENT INLINE FOR RECIPE
# ============================================================
class CommentInline(admin.TabularInline):
    """
    Inline editing for comments within recipe admin
    """
    model = Comment
    extra = 0
    fields = ['user', 'text', 'likes_count', 'created_at']
    readonly_fields = ['created_at']


# ============================================================
# RATING INLINE FOR RECIPE
# ============================================================
class RatingInline(admin.TabularInline):
    """
    Inline editing for ratings within recipe admin
    """
    model = Rating
    extra = 0
    fields = ['user', 'score', 'created_at']
    readonly_fields = ['created_at']


# ============================================================
# RECIPE ADMIN (MAIN MODEL)
# ============================================================
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin interface for Recipe model with comprehensive customization
    """
    list_display = [
        'title',
        'author',
        'category',
        'difficulty_badge',
        'time_display',
        'servings',
        'engagement_display',
        'published_status',
        'created_at'
    ]
    
    list_filter = [
        'category',
        'difficulty',
        'published',
        'created_at',
        ('tags', admin.RelatedOnlyFieldListFilter),
        ('author', admin.RelatedOnlyFieldListFilter),
    ]
    
    search_fields = ['title', 'description', 'ingredients', 'instructions', 'author__username']
    
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'likes_count', 'rating_average']
    
    fieldsets = (
        ('Recipe Information', {
            'fields': ('title', 'description', 'author', 'category', 'published')
        }),
        ('Content', {
            'fields': ('ingredients', 'instructions', 'image')
        }),
        ('Details', {
            'fields': ('difficulty', 'prep_time', 'cook_time', 'servings', 'tags')
        }),
        ('Engagement Metrics', {
            'fields': ('views_count', 'likes_count', 'rating_average'),
            'description': 'Read-only engagement statistics'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [RatingInline, CommentInline]
    
    filter_horizontal = ['tags']
    
    def difficulty_badge(self, obj):
        """Display difficulty level with color coding"""
        colors = {
            'easy': '#70bf2b',
            'medium': '#ffd966',
            'hard': '#ef5350'
        }
        color = colors.get(obj.difficulty, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_difficulty_display()
        )
    difficulty_badge.short_description = 'Difficulty'
    
    def time_display(self, obj):
        """Display total cooking time"""
        total = obj.get_total_time()
        return format_html(
            '<span style="color: #417690;">⏱ {} mins</span>',
            total
        )
    time_display.short_description = 'Total Time'
    
    def engagement_display(self, obj):
        """Display views and likes"""
        return format_html(
            '<span style="color: #666;">👁 {} | ❤️ {}</span>',
            obj.views_count,
            obj.likes_count
        )
    engagement_display.short_description = 'Engagement'
    
    def published_status(self, obj):
        """Display publish status"""
        color = '#70bf2b' if obj.published else '#999'
        status = '✓ Published' if obj.published else '✗ Draft'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    published_status.short_description = 'Status'
    
    def rating_average(self, obj):
        """Display average rating"""
        avg = obj.get_average_rating()
        if avg > 0:
            stars = '⭐' * int(avg) + ('½' if avg % 1 >= 0.5 else '')
            return format_html(
                '<span>{} ({:.1f}/5)</span>',
                stars,
                avg
            )
        return 'No ratings yet'
    rating_average.short_description = 'Average Rating'


# ============================================================
# COMMENT ADMIN
# ============================================================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for Comment model
    """
    list_display = ['user', 'recipe_title', 'comment_preview', 'likes_count', 'created_at']
    list_filter = ['created_at', 'likes_count', ('recipe__category', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['user__username', 'recipe__title', 'text']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('recipe', 'user', 'text')
        }),
        ('Engagement', {
            'fields': ('likes_count',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def recipe_title(self, obj):
        """Display recipe title as link"""
        return format_html(
            '<a href="/admin/recipes/recipe/{}/change/">{}</a>',
            obj.recipe.id,
            obj.recipe.title
        )
    recipe_title.short_description = 'Recipe'
    
    def comment_preview(self, obj):
        """Display truncated comment text"""
        text = obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
        return format_html(
            '<span style="color: #666;">"{}"</span>',
            text
        )
    comment_preview.short_description = 'Comment'


# ============================================================
# RATING ADMIN
# ============================================================
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Admin interface for Rating model
    """
    list_display = ['user', 'recipe_title', 'score_display', 'created_at']
    list_filter = ['score', 'created_at', ('recipe__category', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['user__username', 'recipe__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Rating Information', {
            'fields': ('recipe', 'user', 'score')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def recipe_title(self, obj):
        """Display recipe title as link"""
        return format_html(
            '<a href="/admin/recipes/recipe/{}/change/">{}</a>',
            obj.recipe.id,
            obj.recipe.title
        )
    recipe_title.short_description = 'Recipe'
    
    def score_display(self, obj):
        """Display star rating"""
        stars = '⭐' * obj.score
        return format_html(
            '<span style="font-size: 16px;">{} ({}/5)</span>',
            stars,
            obj.score
        )
    score_display.short_description = 'Rating'