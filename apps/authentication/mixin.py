class UserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user:
            if user.is_active:
                return super(UserMixin, self).dispatch(request, *args, **kwargs)
            else:
                logout(self.request)
        return HttpResponseRedirect(reverse('cv:home'))