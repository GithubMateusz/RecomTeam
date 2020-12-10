from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Sign Up Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            ]
