from rest_framework import serializers
from .models import Recipe, Category, Tag, Comment, Rating


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Converts Category instances to/from JSON.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    Converts Tag instances to/from JSON.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    Includes user information and recipe reference.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_username', 'recipe', 'recipe_title', 'text', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes_count']


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for Rating model.
    Includes user and recipe information.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    recipe_title = serializers.CharField(source='recipe.title', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'user_username', 'recipe', 'recipe_title', 'score', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_score(self, value):
        """Ensure score is between 1 and 5"""
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value


class RecipeDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Recipe model.
    Includes category, tags, and average rating.
    Used for detailed views.
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False
    )
    author_username = serializers.CharField(source='author.username', read_only=True)
    average_rating = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'ingredients', 'instructions',
            'author', 'author_username', 'category', 'category_id', 'tags', 'tag_ids',
            'prep_time', 'cook_time', 'servings', 'difficulty', 'published',
            'created_at', 'updated_at', 'views_count', 'likes_count',
            'average_rating', 'comments_count', 'image'
        ]
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at', 'views_count', 'likes_count']

    def get_average_rating(self, obj):
        """Calculate average rating for the recipe"""
        return obj.get_average_rating()

    def get_comments_count(self, obj):
        """Get count of comments for the recipe"""
        return obj.comment_set.count()


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Recipe model.
    Used for list views with reduced data.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'author', 'author_username', 'category', 'category_name',
            'prep_time', 'cook_time', 'servings', 'difficulty', 'published',
            'views_count', 'likes_count', 'average_rating', 'image', 'created_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'views_count', 'likes_count']

    def get_average_rating(self, obj):
        """Calculate average rating for the recipe"""
        return obj.get_average_rating()
