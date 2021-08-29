from django.contrib.auth import views as auth_views

from apps.authentication.forms import LoginForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'authentication/login.html'
