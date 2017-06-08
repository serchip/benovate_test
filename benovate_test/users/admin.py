from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User


class NewUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class NewUserAdmin(UserAdmin):
    form = NewUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('INN', 'balance')}),
    )
    list_display = UserAdmin.list_display + ('INN', 'balance')


admin.site.register(User, NewUserAdmin)
