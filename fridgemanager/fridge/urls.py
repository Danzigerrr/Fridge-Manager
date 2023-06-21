from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.all_products, name='all_products'),

]
