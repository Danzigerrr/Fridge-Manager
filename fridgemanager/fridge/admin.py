from django.contrib import admin
from .models import Product
from .models import FridgeUser
from .models import Fridge


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'expire_date', 'amount', 'amount_unit')  # columns in admin view
    ordering = ('name',)  # sorting; this comma must be here!
    search_fields = ['name']


@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    fields = (('name', ), 'description', 'owners')  # creating page
    list_display = ('name', 'created_date')  # main page view
    list_filter = ('name', 'created_date')
    ordering = ('name',)  # default sort order
    search_fields = ['name']


@admin.register(FridgeUser)
class FridgeUserAdmin(admin.ModelAdmin):
    fields = (('first_name', 'last_name'), 'email')
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('first_name', 'last_name')
    ordering = ('first_name', 'last_name', )
    search_fields = ('first_name', 'last_name', 'email')