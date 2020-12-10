from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import View

from ..tokens import account_activation_token


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Your account have been confirmed.')
            return redirect('home')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('home')
