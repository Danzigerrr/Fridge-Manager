from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.all_products, name='all_products'),
    path('products/add', views.add_product, name='add_product'),

    path('fridges/', views.all_fridges, name='all_fridges'),
    path('fridges/add', views.add_fridge, name='add_fridge'),
    path('fridges/<fridge_id>/detail', views.fridge_detail, name='fridge_detail'),
    path('fridges/<fridge_id>/update', views.fridge_update, name='fridge_update'),

]
