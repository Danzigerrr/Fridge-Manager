from django.contrib import admin
from .models import Product
from .models import Fridge
from .models import Recipe


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'expire_date', 'amount', 'fridge', 'created_date')  # columns in admin view
    ordering = ('name', )  # sorting; this comma must be here!
    search_fields = ['name']


@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    fields = (('name',), 'description', 'owners', 'invitation_token', )  # creating page
    list_display = ('name', 'created_date', 'invitation_token',)  # main page view
    list_filter = ('name', 'created_date')
    ordering = ('name',)  # default sort order
    search_fields = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('title', 'image_link', 'link', 'api_likes', 'saved_by')  # creating page
    list_display = ('id', 'title',)  # main page view
    list_filter = ('title',)
    ordering = ('title',)  # default sort order
    search_fields = ['title']

