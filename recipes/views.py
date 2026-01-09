from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Recipe, Category, Tag, Comment, Rating, Profile
from .forms import RecipeForm, CommentForm, RatingForm, ProfileForm
from django.db.models import Avg

def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'recipes/home.html', {'recipes': recipes, 'categories': categories, 'tags': tags})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all()
    ratings = recipe.ratings.all()
    average_rating = ratings.aggregate(Avg('score'))['score__avg'] or 0

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            rating_form = RatingForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added!')
                return redirect('recipe_detail', pk=pk)
            if rating_form.is_valid():
                rating, created = Rating.objects.get_or_create(
                    recipe=recipe, user=request.user,
                    defaults={'score': rating_form.cleaned_data['score']}
                )
                if not created:
                    rating.score = rating_form.cleaned_data['score']
                    rating.save()
                messages.success(request, 'Rating updated!')
                return redirect('recipe_detail', pk=pk)
        else:
            messages.error(request, 'You must be logged in to comment or rate.')
            return redirect('login')
    else:
        comment_form = CommentForm()
        rating_form = RatingForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'average_rating': average_rating,
        'comment_form': comment_form,
        'rating_form': rating_form,
    })

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Recipe created!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipes/create_recipe.html', {'form': form})

@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated!')
            return redirect('recipe_detail', pk=pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'recipes/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    recipes = category.recipe_set.all()
    return render(request, 'recipes/category_detail.html', {'category': category, 'recipes': recipes})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'recipes/profile.html', {'profile': profile, 'recipes': recipes})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'recipes/edit_profile.html', {'form': form})

from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create profile
            messages.success(request, 'Account created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})