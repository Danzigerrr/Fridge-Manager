import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Fridge, Product, Recipe


class FridgeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.fridge = Fridge.objects.create(
            name='Test Fridge',
            description='Test description',
            invitation_token=uuid.uuid4(),
        )
        self.fridge.owners.add(self.user)

    def test_fridge_str_representation(self):
        self.assertEqual(str(self.fridge), 'Test Fridge')

    def test_fridge_owners(self):
        self.assertEqual(self.fridge.owners.count(), 1)
        self.assertEqual(self.fridge.owners.first(), self.user)


class ProductModelTest(TestCase):
    def setUp(self):
        self.fridge = Fridge.objects.create(name='Test Fridge')
        self.product = Product.objects.create(
            name='Test Product',
            expire_date='2023-12-31',
            amount=1.5,
            amount_unit=Product.GRAMS,
            fridge=self.fridge,
        )

    def test_product_str_representation(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_amount_unit_choices(self):
        choices = dict(Product.AMOUNT_UNIT_VALUES)
        self.assertIn(self.product.amount_unit, choices)

    def test_product_fridge_relationship(self):
        self.assertEqual(self.product.fridge, self.fridge)


class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            image_link='http://example.com/image.png',
            link='http://example.com/recipe',
            api_likes=42,
        )

    def test_recipe_str_representation(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_recipe_favourite_by_users(self):
        self.assertEqual(self.recipe.favourite_by.count(), 0)

    def test_recipe_api_likes(self):
        self.assertEqual(self.recipe.api_likes, 42)
