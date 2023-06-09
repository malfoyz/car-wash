from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError('Email должен быть указан')

        # Устанавливаем значение поля username в None
        extra_fields.setdefault('username', None)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с указанным адресом электронной почты и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    """
    Модель кастомного пользователя

    Доп. атрибуты:
        patronymic (str): Отчество пользователя.
        is_send_notify (bool): Отправлять ли письмо после завершения заказа.
    """

    username = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        editable=False,
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_("email address"),
    )
    patronymic = models.CharField(
        max_length=50,
        default='',
        verbose_name=_('Отчество'),
    )
    is_send_notify = models.BooleanField(
        default=True,
        verbose_name=_('Отправлять письма'),
    )
    groups = models.ManyToManyField(
        to=Group,
        verbose_name=_("Группы"),
        default=3,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )

    # Устанавливаем адрес электронной почты в качестве уникального идентификатора пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name} {self.patronymic}'
