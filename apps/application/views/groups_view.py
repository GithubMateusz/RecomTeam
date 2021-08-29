from django.views.generic import ListView

from apps.application.models import Group, Statistics


class GroupsView(ListView):
    model = Group
    template_name = 'application/groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        user_statistics = Statistics.objects.filter(user=self.request.user)
        return Group.objects.filter(
            grouprelationships__user_statistics__in=user_statistics).exclude(
            owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['your_groups'] = Group.objects.filter(owner=self.request.user)
        return context
