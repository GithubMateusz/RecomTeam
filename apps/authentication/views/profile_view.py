from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.authentication.forms import ProfileForm
from apps.authentication.models import UserProfile


class ProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'authentication/profile.html'

    def get(self, request, **kwargs):
        self.object = request.user
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return self.request.user
