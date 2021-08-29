from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserProfileManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)


class UserProfile(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    email = models.EmailField(_('email address'), max_length=255, unique=True)
    email_confirmed = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = UserProfileManager()

    def __str__(self):
        return self.email
