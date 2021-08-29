from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView

from apps.authentication.forms import SignupForm
from apps.authentication.tokens import account_activation_token
from django.conf import settings


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'authentication/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            if settings.EMAIL_SENDING:
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your MySite Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)

                messages.success(request, 'Please Confirm your email to complete registration.')
            else:
                user.save()
                user.email_confirmed = True
                user.save()
                messages.success(request, 'Możesz się teraz zalogować.')

            return redirect('login')

        return render(request, self.template_name, {'form': form})
