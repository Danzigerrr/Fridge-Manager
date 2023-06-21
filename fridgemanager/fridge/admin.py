from django.contrib import admin
from .models import Product
from .models import FridgeUser
from .models import Fridge

admin.site.register(Product)
admin.site.register(FridgeUser)
admin.site.register(Fridge)
