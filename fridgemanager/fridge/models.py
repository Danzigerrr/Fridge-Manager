from django.db import models
from django.contrib.auth.models import User
import uuid


class Fridge(models.Model):
    name = models.CharField('Fridge name', max_length=100)
    created_date = models.DateTimeField('Creation date in the system', auto_now_add=True)
    description = models.CharField('Details about the fridge', max_length=200, blank=True)
    owners = models.ManyToManyField(User, blank=True)  # one to many
    invitation_token = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.name


class Product(models.Model):
    PIECES = 'Pieces'
    GRAMS = 'Grams'
    KILOGRAMS = 'Kilograms'
    CARTON = "Carton"
    BOTTLE = "Bottle"
    JAR = "Jar"
    CAN = "Can"
    PACKAGE = "Package"
    CONTAINER = "Container"
    AMOUNT_UNIT_VALUES = [
        (PIECES, 'Pieces'),
        (GRAMS, 'Grams'),
        (KILOGRAMS, 'Kilograms'),
        (CARTON, 'Carton'),
        (BOTTLE, 'Bottle'),
        (JAR, 'Jar'),
        (CAN, 'Can'),
        (PACKAGE, 'Package'),
        (CONTAINER, 'Container')
    ]

    name = models.CharField('Product name', max_length=100)
    expire_date = models.DateField('Expiration date of the product')
    amount = models.FloatField('Amount of the product stored')
    amount_unit = models.CharField(
        max_length=32,
        choices=AMOUNT_UNIT_VALUES,
        default=GRAMS,
    )
    description = models.CharField('Details about the ingredient', max_length=100, blank=True, null=True)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, null=True)  # one to many
    created_date = models.DateTimeField('Creation date in the system', auto_now_add=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField('Recipe title', max_length=100)
    image_link = models.CharField('Link to image', max_length=300)
    link = models.CharField('Link to recipe', max_length=300)
    api_likes = models.IntegerField('Likes by API users', null=True)

    # if the recipe is saved by any user, do not delete it from the database
    if_saved = models.BooleanField(default=False)
    saved_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

