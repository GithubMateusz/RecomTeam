from django.urls import path
from django.contrib.auth import views as auth_views

from .views.acitvate_account import ActivateAccount
from .views.login import LoginView
from .views.profile import ProfileView
from .views.signup import SignupView

urlpatterns = [
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]
