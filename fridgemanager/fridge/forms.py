from django import forms
from django.forms import ModelForm
from .models import Fridge
from .models import Product


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
    # TODO: get only fridges available for this suer
    fridge = forms.ModelChoiceField(queryset=Fridge.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))

    amount_unit = forms.ChoiceField(choices=Product.AMOUNT_UNIT_VALUES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = "__all__"
        # fields = ('name', 'description')
        labels = {
            'name': '',
            'expire_date': '',
            'amount': '',
            'amount_unit': '',
            'description': '',
            'fridge': '',
        }

        # widgets are used for styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'expire_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expiration date'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'amount_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product description'}),
            'fridge': forms.Select(attrs={'class': 'form-control'}),
        }
