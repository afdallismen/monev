from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
]
