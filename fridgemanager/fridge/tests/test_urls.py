import datetime

import pytest
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User  # Assuming you are using Django's User model
from ..models import *


class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)

    def test_home(self):
        url = reverse("home")
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.context["request"].path == "/"

    def test_product_list(self):
        url = reverse("product_list")
        response = self.client.get(url)
        assert response.status_code == 200
        # Add more assertions as needed for the "product_list" view

    def test_product_add(self):
        url = reverse("product_add")
        response = self.client.get(url)
        assert response.status_code == 200
        # Add more assertions as needed for the "product_add" view

    def test_product_detail(self):
        # Create a test fridge with the test user as one of the owners
        test_fridge = Fridge.objects.create(name='Test Fridge')
        test_fridge.owners.add(self.user)

        # Create a test product associated with the test fridge
        test_product = Product.objects.create(
            name='Test Product',
            expire_date='2023-12-31',
            amount=1.5,
            amount_unit=Product.GRAMS,
            fridge=test_fridge,
        )

        # Get the URL for viewing the product detail
        url = reverse('product_detail', args=[test_product.id])

        # Send a GET request to view the product detail
        response = self.client.get(url)

        # Check if the response contains the product information
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, test_product.name)

    def test_product_update(self):
        # Create a test fridge with the test user as one of the owners
        test_fridge = Fridge.objects.create(name='Test Fridge')
        test_fridge.owners.add(self.user)

        # Create a test product associated with the test fridge
        test_product = Product.objects.create(
            name='Test Product',
            expire_date='2023-12-31',
            amount=1.5,
            amount_unit=Product.GRAMS,
            fridge=test_fridge,
        )

        # Get the URL for updating the product
        url = reverse('product_update', args=[test_product.id])

        # Send a GET request to view the product update form
        response = self.client.get(url)

        # Check if the response contains the product update form
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'id="id_name"')
        self.assertContains(response, 'id="id_expire_date"')
        # Add more assertions for other fields if needed

        # Prepare data for updating the product
        updated_data = {
            'name': 'Updated Product Name',
            'expire_date': '2024-01-01',
            'amount': 2.0,
            'amount_unit': Product.KILOGRAMS,
            'fridge': test_fridge.id,
        }

        # Send a POST request to update the product
        response = self.client.post(url, data=updated_data)

        # Check if the product is updated successfully
        self.assertEqual(response.status_code, 302)  # Assuming a successful update redirects to another page
        updated_product = Product.objects.get(id=test_product.id)
        self.assertEqual(updated_product.name, updated_data['name'])
        self.assertEqual(str(updated_product.expire_date), updated_data['expire_date'])
        self.assertEqual(updated_product.amount, updated_data['amount'])
        self.assertEqual(updated_product.amount_unit, updated_data['amount_unit'])
        self.assertEqual(updated_product.fridge, test_fridge)

    def test_product_delete(self):
        # Create a test fridge with the test user as one of the owners
        test_fridge = Fridge.objects.create(name='Test Fridge')
        test_fridge.owners.add(self.user)

        # Create a test product associated with the test fridge
        test_product = Product.objects.create(
            name='Test Product',
            expire_date='2023-12-31',
            amount=1.5,
            amount_unit=Product.GRAMS,
            fridge=test_fridge,
        )

        # Make sure you are logged in as the test user
        self.client.login(username='testuser', password='testpassword')

        # Get the URL for deleting the test product
        url = reverse('product_delete', args=[test_product.id])

        # Send a POST request to delete the product
        response = self.client.post(url)

        # Check if the product is deleted successfully
        self.assertEqual(response.status_code, 302)  # Assuming a successful delete redirects to another page
        self.assertFalse(Product.objects.filter(id=test_product.id).exists())

    def test_product_search(self):
        url = reverse("product_search")
        response = self.client.get(url)
        assert response.status_code == 200
