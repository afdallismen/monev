from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

urlpatterns = [
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('', include('main.urls')),
    path('', views.LoginView.as_view(), name="login")
]
