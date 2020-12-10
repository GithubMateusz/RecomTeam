from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'application/home.html')

    def post(self, request, *args, **kwargs):
        pass
