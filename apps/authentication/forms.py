from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.template.defaultfilters import capfirst
from django.utils.translation import gettext_lazy as _

from apps.authentication.models import UserProfile


class LoginForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', initial="")
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.email_field = UserProfile._meta.get_field(UserProfile.EMAIL_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.email_field.verbose_name},
        )


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address', initial="")

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
        ]


class AdminUserProfileCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserProfile
        fields = ('username', 'email',)


class AdminUserChangeChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email',)
