from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Recipe, Category, Comment, Rating
from .serializers import (
    RecipeListSerializer, RecipeDetailSerializer, CategorySerializer,
    CommentSerializer, RatingSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Category model.
    Supports: GET (list & detail), POST (create), PUT (update), DELETE (delete)
    
    Endpoints:
    - GET /api/categories/ - List all categories
    - POST /api/categories/ - Create new category
    - GET /api/categories/{id}/ - Retrieve specific category
    - PUT /api/categories/{id}/ - Update category
    - DELETE /api/categories/{id}/ - Delete category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def recipes(self, request, pk=None):
        """
        Get all recipes in a specific category.
        GET /api/categories/{id}/recipes/
        """
        category = self.get_object()
        recipes = category.recipe_set.all()
        serializer = RecipeListSerializer(recipes, many=True)
        return Response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Recipe model.
    Supports: GET (list & detail), POST (create), PUT (update), DELETE (delete)
    
    Endpoints:
    - GET /api/recipes/ - List all recipes (paginated)
    - POST /api/recipes/ - Create new recipe
    - GET /api/recipes/{id}/ - Retrieve specific recipe
    - PUT /api/recipes/{id}/ - Update recipe
    - DELETE /api/recipes/{id}/ - Delete recipe
    - GET /api/recipes/{id}/comments/ - Get recipe comments
    - POST /api/recipes/{id}/comments/ - Add comment to recipe
    - GET /api/recipes/{id}/ratings/ - Get recipe ratings
    - POST /api/recipes/{id}/ratings/ - Add rating to recipe
    """
    queryset = Recipe.objects.filter(published=True).order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'difficulty', 'published']
    search_fields = ['title', 'description', 'ingredients']
    ordering_fields = ['created_at', 'views_count', 'likes_count']

    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return RecipeListSerializer

    def perform_create(self, serializer):
        """Set the author to the current user when creating a recipe"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Only allow recipe author to update"""
        recipe = self.get_object()
        if recipe.author != self.request.user:
            return Response(
                {'detail': 'Only the recipe author can update this recipe.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a specific recipe.
        GET /api/recipes/{id}/comments/
        """
        recipe = self.get_object()
        comments = recipe.comment_set.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        """
        Add a comment to a recipe.
        POST /api/recipes/{id}/add_comment/
        Body: {"text": "comment text"}
        """
        recipe = self.get_object()
        text = request.data.get('text')

        if not text:
            return Response(
                {'detail': 'Text field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        comment = Comment.objects.create(
            user=request.user,
            recipe=recipe,
            text=text
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        """
        Get all ratings for a specific recipe.
        GET /api/recipes/{id}/ratings/
        """
        recipe = self.get_object()
        ratings = recipe.rating_set.all().order_by('-created_at')
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_rating(self, request, pk=None):
        """
        Add or update a rating for a recipe.
        POST /api/recipes/{id}/add_rating/
        Body: {"score": 4}
        """
        recipe = self.get_object()
        score = request.data.get('score')

        if not score:
            return Response(
                {'detail': 'Score field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            score = int(score)
            if not (1 <= score <= 5):
                raise ValueError()
        except (ValueError, TypeError):
            return Response(
                {'detail': 'Score must be an integer between 1 and 5.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            recipe=recipe,
            defaults={'score': score}
        )
        serializer = RatingSerializer(rating)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        """
        Get average rating for a recipe.
        GET /api/recipes/{id}/average_rating/
        """
        recipe = self.get_object()
        avg_rating = recipe.get_average_rating()
        return Response({
            'id': recipe.id,
            'title': recipe.title,
            'average_rating': avg_rating,
            'total_ratings': recipe.rating_set.count()
        })


class CommentViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Comment model.
    Supports: GET (list & detail), POST (create), PUT (update), DELETE (delete)
    
    Endpoints:
    - GET /api/comments/ - List all comments
    - POST /api/comments/ - Create new comment
    - GET /api/comments/{id}/ - Retrieve specific comment
    - PUT /api/comments/{id}/ - Update comment
    - DELETE /api/comments/{id}/ - Delete comment
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set the user to the current user when creating a comment"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Only allow comment author to update"""
        comment = self.get_object()
        if comment.user != self.request.user:
            return Response(
                {'detail': 'Only the comment author can update this comment.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Only allow comment author to delete"""
        if instance.user != self.request.user:
            return Response(
                {'detail': 'Only the comment author can delete this comment.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()


class RatingViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Rating model.
    Supports: GET (list & detail), POST (create), PUT (update), DELETE (delete)
    
    Endpoints:
    - GET /api/ratings/ - List all ratings
    - POST /api/ratings/ - Create new rating
    - GET /api/ratings/{id}/ - Retrieve specific rating
    - PUT /api/ratings/{id}/ - Update rating
    - DELETE /api/ratings/{id}/ - Delete rating
    """
    queryset = Rating.objects.all().order_by('-created_at')
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Set the user to the current user when creating a rating"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Only allow rating author to update"""
        rating = self.get_object()
        if rating.user != self.request.user:
            return Response(
                {'detail': 'Only the rating author can update this rating.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Only allow rating author to delete"""
        if instance.user != self.request.user:
            return Response(
                {'detail': 'Only the rating author can delete this rating.'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
