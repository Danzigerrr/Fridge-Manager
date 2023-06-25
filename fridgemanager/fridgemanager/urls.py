from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fridge.urls')),
    path('members/', include('django.contrib.auth.urls')),  # authenticate of users
    path('members/', include('members.urls')),
]

# Configure Admin Titles
admin.site.site_header = "Fridge Manager Administration Page"
admin.site.site_title = "Fridge Manager Admin Panel"
admin.site.index_title = "Welcome to the Admin Area of Fridge Manager"
