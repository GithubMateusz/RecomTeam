from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

from apps.authentication.models import UserProfile


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username__iexact=username) | Q(email__iexact=email))
        except UserProfile.DoesNotExist:
            UserProfile().set_password(password)
        except MultipleObjectsReturned:
            return UserProfile.objects.filter(Q(username=username) | Q(email=email)).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserProfile.objects.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
