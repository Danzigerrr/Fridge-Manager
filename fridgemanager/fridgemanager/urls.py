from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fridge.urls')),
    path('members/', include('django.contrib.auth.urls')),  # authenticate of users
    path('members/', include('members.urls')),
]
