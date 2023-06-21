from django.db import models


class FridgeUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField('User email', max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Fridge(models.Model):
    name = models.CharField('Fridge name', max_length=100)
    created_date = models.DateTimeField('Registration date in the system')
    description = models.CharField('Details about the fridge', max_length=200)
    owners = models.ManyToManyField(FridgeUser, blank=True)  # one to many

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Product name', max_length=100)
    expire_date = models.DateTimeField('Expiration date of the product')
    amount = models.FloatField('Amount of the product stored')
    description = models.CharField('Details about the ingredient', max_length=100, blank=True, null=True)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE, blank=True, null=True)  # one to many

    def __str__(self):
        return self.name






