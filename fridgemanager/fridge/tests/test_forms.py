from django.test import TestCase
from ..forms import *
from datetime import datetime


class TestFridgeForm(TestCase):

    def test_valid_form(self):
        # Create test data
        form_data = {
            'name': 'Test Fridge',
            'description': 'Test description',
        }

        # Create the form with the test data
        form = FridgeForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        # Create an empty form
        form = FridgeForm(data={})

        # Check if the form is not valid
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # One field is required

    def test_form_labels(self):
        # Check if the form labels are as expected
        form = FridgeForm()
        self.assertEqual(form.fields['name'].label, '')
        self.assertEqual(form.fields['description'].label, '')

    def test_form_widgets(self):
        # Check if the form widgets are as expected
        form = FridgeForm()
        self.assertEqual(form.fields['name'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['name'].widget.attrs.get('placeholder'), 'Fridge name')
        self.assertEqual(form.fields['description'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['description'].widget.attrs.get('placeholder'), 'Description')


class TestProductForm(TestCase):

    def setUp(self):
        # Create a fridge instance for association
        fridge = Fridge.objects.create(name='Test Fridge')

        self.product_data = {
            'name': 'Test Product',
            'expire_date': '2021-12-31',
            'amount': 100,
            'amount_unit': 'Grams',
            'description': 'Test description',
            'fridge': fridge.id,  # Use the created fridge instance ID
        }

    def test_valid_form(self):
        form = ProductForm(data=self.product_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = self.product_data.copy()
        form_data['name'] = ''  # make the form invalid
        form = ProductForm(data=form_data)
        if form.is_valid():
            print("Unexpected valid form")
            print(form.errors)
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form = ProductForm(data=self.product_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

        product = form.save()

        # Convert the string date to datetime.date object
        expire_date_str = self.product_data['expire_date']
        expire_date = datetime.strptime(expire_date_str, '%Y-%m-%d').date()

        self.assertEqual(product.expire_date, expire_date)
        self.assertEqual(product.name, self.product_data['name'])

    def test_form_widgets(self):
        form = ProductForm()
        self.assertIn('class="form-control"', str(form['amount_unit']))
        self.assertIn('type="date"', str(form['expire_date']))


