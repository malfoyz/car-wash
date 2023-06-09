from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic',
                  'email', 'is_send_notify', 'groups',)


class CustomUserChangeForm(UserChangeForm):
    """Форма изменения пользователя"""

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'patronymic',
                  'email', 'is_send_notify', 'groups',)
