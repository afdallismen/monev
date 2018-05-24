from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

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
    path('edit/', account_views.edit, name="edit"),
    path(
        'password/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/password_change.html',
            success_url=reverse_lazy('main:index'),
        ),
        name="password_change",
    ),
]
