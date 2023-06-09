from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Редактор модели пользователя"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',)
    list_filter = ('email', 'first_name', 'last_name',)

    add_fieldsets = (
        # *UserAdmin.add_fieldsets,
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'patronymic',
                       'is_send_notify', 'groups', 'password1', 'password2',)
        }),
    )

    fieldsets = (
        # *UserAdmin.fieldsets,
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'patronymic',
                       'is_send_notify', 'groups',)
        }),
    )
