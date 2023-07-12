from django import forms
from django.forms import ModelForm
from .models import Fridge, Product


class FridgeForm(ModelForm):
    class Meta:
        model = Fridge
        # fields = "__all__"
        fields = ('name', 'description')

        labels = {
            'name': '',
            'description': ''
        }

        # widgets are used for styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fridge name'}),  # 'form-control' -> add Bootstrap styles
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }


class ProductForm(forms.ModelForm):
    amount_unit = forms.ChoiceField(choices=Product.AMOUNT_UNIT_VALUES, widget=forms.Select(attrs={'class': 'form-control'}))
    expire_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Product
        fields = "__all__"
        # fields = ('name', 'description')
        labels = {
            'name': '',
            'expire_date': 'YYYY-MM-DD HH:MM:SS',
            'amount': '',
            'amount_unit': ' ',
            'description': '',
            'fridge': '',
        }

        # widgets are used for styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product description'}),
            'fridge': forms.Select(attrs={'class': 'form-control'}),
        }
