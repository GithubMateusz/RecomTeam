from django.http import JsonResponse
from django.views import View

from apps.application.models import Statistics, Invitations, Group, GroupRelationships


class InvitePlayerView(View):
    def post(self, request, *args, **kwargs):
        uuid = request.POST.get('id', None)

        game_name = kwargs.get('game')
        user = request.user
        if uuid:
            try:
                statistics = Statistics.objects.get(uuid=uuid)
                your_statistics = Statistics.objects.get(user=user, game_name=game_name)
                try:
                    group = Group.objects.get(owner=user, game_name=game_name)
                except Group.DoesNotExist:
                    group = Group(game_name=game_name, owner=user)
                    group.save()
                    group_relationships = GroupRelationships(group=group, user_statistics=your_statistics)
                    group_relationships.save()

                invitation = Invitations(group=group, user_statistics=statistics)
                invitation.save()
                return JsonResponse(data={
                    "message": "Zaprosiłeś użytkownika {} do swojej grupy w grze: {}".format(
                        statistics.account_name, game_name)
                })
            except Statistics.DoesNotExist:
                pass

        return JsonResponse(data={"message": "Coś poszło nie tak"})
