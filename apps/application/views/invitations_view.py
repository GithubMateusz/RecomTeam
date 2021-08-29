from django.views.generic import ListView

from django.http import JsonResponse
from django.views import View

from apps.application.models import Statistics, Invitations, GroupRelationships


class InvitationsView(ListView):
    model = Invitations
    template_name = 'application/invitations.html'
    context_object_name = 'invitations'

    def get_queryset(self):
        user_statistics = Statistics.objects.filter(user=self.request.user)
        return Invitations.objects.filter(user_statistics__in=user_statistics)


class ConfirmInvitationView(View):
    def post(self, request, *args, **kwargs):
        uuid = request.POST.get('id', None)
        if uuid:
            try:
                invitation = Invitations.objects.get(uuid=uuid)
                group = invitation.group

                group_relationship = GroupRelationships(user_statistics=invitation.user_statistics, group=group)
                group_relationship.save()

                invitation.delete()
                return JsonResponse(data={
                    "message": "Dołączyłeś do grupy użytkownika {} w grze: {}".format(
                        group.owner, group.game_name)
                })
            except Invitations.DoesNotExist:
                pass

        return JsonResponse(data={"message": "Coś poszło nie tak"})


class CancelInvitationView(View):
    def post(self, request, *args, **kwargs):
        uuid = request.POST.get('id', None)
        if uuid:
            try:
                invitation = Invitations.objects.get(uuid=uuid)
                group = invitation.group

                invitation.delete()
                return JsonResponse(data={
                    "message": "Anulowałeś zaproszenie do grupy użytkownika {} w grze: {}".format(
                        group.owner, group.game_name)
                })
            except Invitations.DoesNotExist:
                pass

        return JsonResponse(data={"message": "Coś poszło nie tak"})
