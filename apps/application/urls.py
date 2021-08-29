from django.urls import path

from .views.get_account_view import GetAccountView
from .views.groups_view import GroupsView
from .views.home_view import HomeView
from .views.invitations_view import InvitationsView, CancelInvitationView, ConfirmInvitationView
from .views.invite_player_view import InvitePlayerView
from .views.referred_players_view import ReferredPlayersView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('groups', GroupsView.as_view(), name='groups'),
    path('invitations', InvitationsView.as_view(), name='invitations'),
    path('invitations/confirm-invitation', ConfirmInvitationView.as_view(), name='confirm_invitation'),
    path('invitations/cancel-invitation', CancelInvitationView.as_view(), name='cancel_invitation'),
    path('<game>/get-account', GetAccountView.as_view(), name='get_account'),
    path('<game>/referred-players', ReferredPlayersView.as_view(), name='referred_players'),
    path('<game>/invite-player', InvitePlayerView.as_view(), name='invite_player'),
]