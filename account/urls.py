from django.contrib.auth import views as auth_views
from django.urls import path

from account import views as account_views


app_name = 'account'
urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='account/login.html',
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('register/', account_views.register, name="register"),
    # path('<string:username>/edit', account_views.edit, name="edit"),
]
