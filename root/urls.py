from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('', include('main.urls')),
]
