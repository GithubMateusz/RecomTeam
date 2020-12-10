from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.views import generic
from django.views.generic import View


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'authentication/login.html', dict(form=form))

    def post(self, request, *args, **kwargs):
        pass
