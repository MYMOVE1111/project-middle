from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from .models import Recipe, Category, Tag, Comment, Rating, Profile
from .forms import RecipeForm, CommentForm, RatingForm, ProfileForm
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator

def home(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    search_query = request.GET.get('q', '').strip()
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query) |
            Q(instructions__icontains=search_query)
        )
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Pagination
    paginator = Paginator(recipes, 6)  # 6 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    recipes_count = Recipe.objects.count()
    users_count = User.objects.count()
    categories_count = Category.objects.count()
    tags_count = Tag.objects.count()
    
    return render(request, 'recipes/home.html', {
        'recipes': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
        'recipes_count': recipes_count,
        'users_count': users_count,
        'categories_count': categories_count,
        'tags_count': tags_count,
        'search_query': search_query,
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all()
    ratings = recipe.ratings.all()
    average_rating = ratings.aggregate(Avg('score'))['score__avg'] or 0

    if request.method == 'POST':
        if request.user.is_authenticated:
            form_type = request.POST.get('form_type')
            
            if form_type == 'comment':
                comment_form = CommentForm(request.POST)
                rating_form = RatingForm()
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.recipe = recipe
                    comment.user = request.user
                    comment.save()
                    messages.success(request, 'Comment added!')
                    return redirect('recipe_detail', pk=pk)
            elif form_type == 'rating':
                comment_form = CommentForm()
                rating_form = RatingForm(request.POST)
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
                comment_form = CommentForm()
                rating_form = RatingForm()
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

def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    recipes = tag.recipes.all()
    return render(request, 'recipes/tag_detail.html', {'tag': tag, 'recipes': recipes})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
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

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')