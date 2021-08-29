from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from apps.application.games.fortnite import fortnite
from apps.application.games.league_of_legends import lol
from apps.authentication.models import UserProfile


class Statistics(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    game_name = models.CharField(max_length=255, blank=False)
    account_name = models.CharField(max_length=255, blank=False)
    points = models.IntegerField(blank=False)
    last_update = models.DateTimeField()

    def update_points(self):
        if self.game_name == "league-of-legends":
            self.points = lol.get_points(self.account_name, "eun1")
        elif self.game_name == "fortnite":
            self.points = fortnite.get_points(self.account_name)
        self.save()


class Group(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    game_name = models.CharField(max_length=255)
    created_ad = models.DateTimeField(auto_now_add=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class Invitations(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user_statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class GroupRelationships(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user_statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
