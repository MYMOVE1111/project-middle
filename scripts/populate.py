import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_sharing.settings')
django.setup()

from recipes.models import Category, Tag, Recipe, Profile
from django.contrib.auth.models import User

# Create categories
cat1, _ = Category.objects.get_or_create(name='Italian')
cat2, _ = Category.objects.get_or_create(name='Mexican')
cat3, _ = Category.objects.get_or_create(name='Desserts')
cat4, _ = Category.objects.get_or_create(name='Asian')
cat5, _ = Category.objects.get_or_create(name='Breakfast')
cat6, _ = Category.objects.get_or_create(name='Healthy')

# Create tags
tag1, _ = Tag.objects.get_or_create(name='Vegetarian')
tag2, _ = Tag.objects.get_or_create(name='Spicy')
tag3, _ = Tag.objects.get_or_create(name='Quick')
tag4, _ = Tag.objects.get_or_create(name='Easy')
tag5, _ = Tag.objects.get_or_create(name='Gluten-Free')
tag6, _ = Tag.objects.get_or_create(name='Low-Carb')

# Create users
user1, _ = User.objects.get_or_create(username='chef_mario', defaults={'email': 'mario@example.com'})
user2, _ = User.objects.get_or_create(username='cook_sarah', defaults={'email': 'sarah@example.com'})

# Create profiles
Profile.objects.get_or_create(user=user1)
Profile.objects.get_or_create(user=user2)

# Create recipes
recipe1 = Recipe.objects.create(
    author=user1,
    title='Classic Spaghetti Carbonara',
    description='A traditional Italian pasta dish with eggs, cheese, and pancetta.',
    ingredients='200g spaghetti\n100g pancetta\n2 eggs\n50g Parmesan cheese\nBlack pepper',
    instructions='1. Cook spaghetti in salted boiling water.\n2. Fry pancetta until crispy.\n3. Mix eggs and cheese.\n4. Combine with hot pasta.\n5. Season with pepper.',
    category=cat1,
    prep_time=10,
    cook_time=20,
    servings=2,
    difficulty='easy'
)
recipe1.tags.add(tag3)

recipe2 = Recipe.objects.create(
    author=user2,
    title='Chicken Tacos',
    description='Delicious Mexican tacos with seasoned chicken.',
    ingredients='500g chicken breast\n2 tbsp taco seasoning\n8 tortillas\n1 onion\n1 tomato\nLettuce',
    instructions='1. Season chicken and cook.\n2. Chop vegetables.\n3. Warm tortillas.\n4. Assemble tacos.',
    category=cat2,
    prep_time=15,
    cook_time=20,
    servings=4,
    difficulty='easy'
)
recipe2.tags.add(tag2)

recipe3 = Recipe.objects.create(
    author=user1,
    title='Chocolate Chip Cookies',
    description='Chewy and delicious homemade cookies.',
    ingredients='2 cups flour\n1 cup butter\n1 cup sugar\n1 egg\n1 tsp vanilla\n1 cup chocolate chips',
    instructions='1. Cream butter and sugar.\n2. Add egg and vanilla.\n3. Mix in flour.\n4. Add chocolate chips.\n5. Bake at 350F for 10-12 min.',
    category=cat3,
    prep_time=15,
    cook_time=12,
    servings=24,
    difficulty='easy'
)
recipe3.tags.add(tag1, tag3)

recipe4 = Recipe.objects.create(
    author=user2,
    title='Pad Thai',
    description='Authentic Thai stir-fried noodles with shrimp and peanuts.',
    ingredients='200g rice noodles\n200g shrimp\n2 eggs\n1 cup bean sprouts\n1/4 cup peanuts\n2 tbsp fish sauce\n1 tbsp tamarind paste',
    instructions='1. Soak noodles in hot water.\n2. Stir-fry shrimp and eggs.\n3. Add noodles and sauce.\n4. Mix in bean sprouts and peanuts.\n5. Serve hot.',
    category=cat4,
    prep_time=10,
    cook_time=15,
    servings=2,
    difficulty='medium'
)
recipe4.tags.add(tag2, tag4)

recipe5 = Recipe.objects.create(
    author=user1,
    title='Avocado Toast',
    description='Simple and healthy breakfast with avocado on toasted bread.',
    ingredients='2 slices bread\n1 avocado\n1 tomato\nSalt and pepper\nOlive oil',
    instructions='1. Toast the bread.\n2. Mash avocado and spread on toast.\n3. Top with sliced tomato.\n4. Season with salt, pepper, and olive oil.',
    category=cat5,
    prep_time=5,
    cook_time=5,
    servings=1,
    difficulty='easy'
)
recipe5.tags.add(tag1, tag3, tag5)

recipe6 = Recipe.objects.create(
    author=user2,
    title='Grilled Salmon',
    description='Healthy grilled salmon with herbs and lemon.',
    ingredients='4 salmon fillets\n2 tbsp olive oil\n1 lemon\nFresh herbs (dill, parsley)\nSalt and pepper',
    instructions='1. Season salmon with salt, pepper, and herbs.\n2. Drizzle with olive oil and lemon juice.\n3. Grill for 4-5 minutes per side.\n4. Serve with lemon wedges.',
    category=cat6,
    prep_time=10,
    cook_time=10,
    servings=4,
    difficulty='easy'
)
recipe6.tags.add(tag5, tag6)