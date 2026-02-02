from django.core.management.base import BaseCommand
from recipes.models import Category, Tag, Recipe, Profile
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populate the database with sample recipes'

    def handle(self, *args, **options):
        # Create categories
        cat1, _ = Category.objects.get_or_create(name='Italian')
        cat2, _ = Category.objects.get_or_create(name='Mexican')
        cat3, _ = Category.objects.get_or_create(name='Desserts')

        # Create tags
        tag1, _ = Tag.objects.get_or_create(name='Vegetarian')
        tag2, _ = Tag.objects.get_or_create(name='Spicy')
        tag3, _ = Tag.objects.get_or_create(name='Quick')

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
            category=cat1
        )
        recipe1.tags.add(tag3)

        recipe2 = Recipe.objects.create(
            author=user2,
            title='Chicken Tacos',
            description='Delicious Mexican tacos with seasoned chicken.',
            ingredients='500g chicken breast\n2 tbsp taco seasoning\n8 tortillas\n1 onion\n1 tomato\nLettuce',
            instructions='1. Season chicken and cook.\n2. Chop vegetables.\n3. Warm tortillas.\n4. Assemble tacos.',
            category=cat2
        )
        recipe2.tags.add(tag2)

        recipe3 = Recipe.objects.create(
            author=user1,
            title='Chocolate Chip Cookies',
            description='Chewy and delicious homemade cookies.',
            ingredients='2 cups flour\n1 cup butter\n1 cup sugar\n1 egg\n1 tsp vanilla\n1 cup chocolate chips',
            instructions='1. Cream butter and sugar.\n2. Add egg and vanilla.\n3. Mix in flour.\n4. Add chocolate chips.\n5. Bake at 350F for 10-12 min.',
            category=cat3
        )
        recipe3.tags.add(tag1, tag3)

        self.stdout.write(self.style.SUCCESS('Sample recipes added successfully!'))