from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdminUserProfileCreationForm, AdminUserChangeChangeForm
from .models import UserProfile


class UserProfileAdmin(UserAdmin):
    add_form = AdminUserProfileCreationForm
    form = AdminUserChangeChangeForm
    model = UserProfile
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)


admin.site.register(UserProfile, UserProfileAdmin)
