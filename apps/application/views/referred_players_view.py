from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View

from apps.application.models import Statistics, Group, Invitations, GroupRelationships


@method_decorator(login_required, name='dispatch')
class ReferredPlayersView(View):
    template_name = 'application/referred_players.html'

    def get(self, request, *args, **kwargs):
        try:
            your_statistics = Statistics.objects.get(user=request.user, game_name=kwargs.get('game'))
        except Statistics.DoesNotExist:
            return redirect(reverse("get_account", kwargs={"game": kwargs.get('game')}))
        groups = Group.objects.filter(owner=request.user, game_name=kwargs.get('game'))

        statistics_of_other_players = list(Statistics.objects.exclude(
            user=request.user).exclude(
            invitations__group__in=groups).exclude(
            grouprelationships__group__in=groups).filter(
            game_name=kwargs.get('game')
            ).values())
        if statistics_of_other_players:
            statistics_of_other_players = recommendation_algorithm_the_best_first(
                your_statistics.points, statistics_of_other_players)

        return render(request, self.template_name, {'game': kwargs.get('game'),
                                                    'your_statistics': your_statistics,
                                                    "statistics_of_other_players": statistics_of_other_players})

    def post(self, request, *args, **kwargs):
        try:
            your_statistics = Statistics.objects.get(user=request.user, game_name=kwargs.get('game'))
        except Statistics.DoesNotExist:
            return redirect(reverse("get_account", kwargs={"game": kwargs.get('game')}))

        your_statistics.update_points()

        groups = Group.objects.filter(owner=request.user, game_name=kwargs.get('game'))

        statistics_of_other_players = list(Statistics.objects.exclude(
            user=request.user).exclude(
            invitations__group__in=groups).exclude(
            grouprelationships__group__in=groups).filter(
            game_name=kwargs.get('game')
        ).values())
        if statistics_of_other_players:
            statistics_of_other_players = recommendation_algorithm_the_best_first(
                your_statistics.points, statistics_of_other_players)

        return render(request, self.template_name, {'game': kwargs.get('game'),
                                                    'your_statistics': your_statistics,
                                                    "statistics_of_other_players": statistics_of_other_players})



def recommendation_algorithm_the_best_first(your_points, statistics_of_other_players):
    sorted_best_first_statistics_of_other_players = []
    while len(statistics_of_other_players):
        best_player_statistics = __best_first(your_points, statistics_of_other_players)
        sorted_best_first_statistics_of_other_players.append(best_player_statistics)
        statistics_of_other_players.remove(best_player_statistics)

    return sorted_best_first_statistics_of_other_players


def __best_first(your_points, statistics_of_other_players):
    best_player_statistics = None

    for player_statistics in statistics_of_other_players:
        best_player_statistics = __return_better_statistics(your_points, player_statistics, best_player_statistics)

    return best_player_statistics


def __return_better_statistics(your_points, player_statistics, best_player_statistics):
    if best_player_statistics:
        if abs(your_points - player_statistics.get("points")) > abs(your_points - best_player_statistics.get("points")):
            return best_player_statistics
        return player_statistics
    else:
        return player_statistics
