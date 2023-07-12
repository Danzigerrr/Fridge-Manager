from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add', views.product_add, name='product_add'),
    path('products/<product_id>/detail', views.product_detail, name='product_detail'),
    path('products/<product_id>/update', views.product_update, name='product_update'),
    path('products/<product_id>/delete', views.product_delete, name='product_delete'),
    path('products/search', views.products_search, name='product_search'),

    path('fridges/', views.fridge_list, name='fridge_list'),
    path('fridges/add', views.fridge_add, name='fridge_add'),
    path('fridges/<fridge_id>/detail', views.fridge_detail, name='fridge_detail'),
    path('fridges/<fridge_id>/update', views.fridge_update, name='fridge_update'),
    path('fridges/<fridge_id>/delete', views.fridge_delete, name='fridge_delete'),
    path('fridges/<fridge_id>/products', views.fridge_products, name='fridge_products'),
    path('fridges/export_as_text', views.fridges_export_as_text, name='fridges_export_as_text'),
    path('fridges/export_as_csv', views.fridges_export_as_csv, name='fridges_export_as_csv'),
    path('fridges/export_as_pdf', views.fridges_export_as_pdf, name='fridges_export_as_pdf'),

    path('recipes/', views.recipe_saved_list, name='recipe_list'),
    path('recipes/save', views.recipe_save, name='recipe_save'),
    path('recipes/unsave', views.recipe_unsave, name='recipe_unsave'),
    path('recipes/search_by_ingredients', views.get_recipe_from_product_list, name='get_recipe_from_product_list'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
]
