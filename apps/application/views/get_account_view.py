import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from apps.application.forms.get_account_form import GetAccountForm
from apps.application.games.fortnite import fortnite
from apps.application.games.league_of_legends import lol
from apps.application.models import Statistics


@method_decorator(login_required, name='dispatch')
class GetAccountView(FormView):
    template_name = 'application/get_account.html'
    form_class = GetAccountForm

    def get(self, request, *args, **kwargs):
        try:
            user_statistics = Statistics.objects.get(user=request.user, game_name=kwargs.get('game'))
            return redirect(reverse("referred_players", kwargs={"game": kwargs.get('game')}))
        except Statistics.DoesNotExist:
            pass

        return render(request, self.template_name, {'game': kwargs.get('game')})

    def post(self, request, *args, **kwargs):
        try:
            account_name = request.POST.get("account_name")
            if kwargs.get('game') == 'league-of-legends':
                try:
                    user_statistics = Statistics.objects.get(user=request.user, game_name='league-of-legends')
                except Statistics.DoesNotExist:
                    points = lol.get_points(account_name, "eun1")
                    user_statistics = Statistics(
                        user=request.user,
                        game_name='league-of-legends',
                        account_name=account_name,
                        points=points,
                        last_update=timezone.now())
                    user_statistics.save()

                return redirect(reverse("referred_players", kwargs={"game": "league-of-legends"}))

            elif kwargs.get('game') == 'fortnite':
                try:
                    user_statistics = Statistics.objects.get(user=request.user, game_name='fortnite')
                except Statistics.DoesNotExist:
                    points = fortnite.get_points(account_name)
                    user_statistics = Statistics(
                        user=request.user,
                        game_name='fortnite',
                        account_name=account_name,
                        points=points,
                        last_update=timezone.now())
                    user_statistics.save()

                return redirect(reverse("referred_players", kwargs={"game": "fortnite"}))

        except Exception as e:
            print(str(e))
            messages.error(request, 'Account with this name not exist.')
        return render(request, self.template_name, {'game': kwargs.get('game')})

    def form_valid(self, form):
        return super().form_valid(form)
