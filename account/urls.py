from django.contrib.auth import views as auth_views
from django.urls import path

from account import views as account_views


app_name = 'account'
urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='account/login_form.html',
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signin/', account_views.signin, name="signin"),
    path('<str:username>/edit', account_views.edit, name="edit"),
]
