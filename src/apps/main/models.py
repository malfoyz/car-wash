from django.db import models
from django.utils.translation import gettext_lazy as _

from ..users.models import CustomUser


class Brand(models.Model):
    """
    Модель марки

    Атрибуты:
        name (str): Название марки.
    """

    name = models.CharField(
        verbose_name=_('Название'),
        max_length=100,
    )

    class Meta:
        verbose_name = _('Марка')
        verbose_name_plural = _('Марки')
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Car(models.Model):
    """
    Модель машины.

    Атрибуты:
        brand (int): Марка машины.
        model (str): Модель машины.
    """

    brand = models.ForeignKey(
        verbose_name=_('Марка'),
        to='Brand',
        on_delete=models.CASCADE,
        related_name='cars',
        related_query_name='car',
    )
    model = models.CharField(
        verbose_name=_('Модель'),
        max_length=100,
    )

    class Meta:
        verbose_name = _('Машина')
        verbose_name_plural = _('Машины')

    def __str__(self) -> str:
        return f'{self.brand.name} {self.model}'


class ServiceCategory(models.Model):
    """
    Модель категории услуг.

    Атрибуты:
        name (str): Название категории услуг.
    """

    name = models.CharField(
        verbose_name=_('Название'),
        max_length=100,
    )

    class Meta:
        verbose_name = _('Категория услуг')
        verbose_name_plural = _('Категории услуг')

    def __str__(self) -> str:
        return self.name


class Service(models.Model):
    """
    Модель услуги.

    Атрибуты:
        service_category (int): Категория услуги.
        name (str): Название услуги.
        price (int): Цена услуги.
    """

    service_category = models.ForeignKey(
        verbose_name=_('Категория услуг'),
        to='ServiceCategory',
        on_delete=models.PROTECT,
        related_name='services',
        related_query_name='service',
    )
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=100,
    )
    price = models.PositiveIntegerField(
        verbose_name=_('Цена'),
    )

    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')

    def __str__(self) -> str:
        return self.name


class CustomerCar(models.Model):
    """
    Модель машины клиента.

    Атрибуты:
        car (int): Машина клиента.
        customer (int): Клиент, которому принадлежит машина.
        year (int): Год выпуска машины.
        number (str): Номер машины.
        image (str): Фото машины.
    """

    car = models.ForeignKey(
        verbose_name=_('Машина'),
        to='Car',
        on_delete=models.PROTECT,
        related_name='customer_cars',
        related_query_name='customer_car',
    )
    customer = models.ForeignKey(
        verbose_name=_('Клиент'),
        to=CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={'groups__name': 'Клиент'},
        related_name='customer_cars',
        related_query_name='customer_cars',
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_('Год выпуска'),
    )
    number = models.CharField(
        verbose_name=_('Номер'),
        max_length=20,
    )
    image = models.ImageField(
        verbose_name=_('Фото'),
        upload_to='cars/',
        blank=True,
    )

    class Meta:
        verbose_name = _('Машина клиента')
        verbose_name_plural = _('Машины клиентов')

    def __str__(self) -> str:
        return self.number


class Order(models.Model):
    """
    Модель заказа.

    Атрибуты:
        service (int): Услуга заказа.
        customer_car (int): Машина клиента.
        employee (int): Работник, выполняющий заказ.
        administrator (int): Администратор, отвечающий за выполнение заказа.
        status (int): Статус выполнения заказа.
        start_date (datetime): Дата и время начала выполнения заказа.
        end_date (datetime): Дата и время завершения выполнения заказа.
    """

    STATUSES = (
        (0, 'В работе'),
        (1, 'Завершен'),
    )

    service = models.ForeignKey(
        verbose_name=_('Услуга'),
        to='Service',
        on_delete=models.PROTECT,
        related_name='orders',
        related_query_name='order',
    )
    customer_car = models.ForeignKey(
        verbose_name=_('Машина клиента'),
        to='CustomerCar',
        on_delete=models.PROTECT,
        related_name='orders',
        related_query_name='order',
    )
    employee = models.ForeignKey(
        verbose_name=_('Работник'),
        to=CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={'groups__name': 'Работник'},
        related_name='orders',
        related_query_name='order',
    )
    administrator = models.ForeignKey(
        verbose_name=_('Администратор'),
        to=CustomUser,
        on_delete=models.PROTECT,
        limit_choices_to={'groups__name': 'Администратор'},
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=_('Статус'),
        choices=STATUSES,
        default=0,
    )
    start_date = models.DateTimeField(
        verbose_name=_('Дата и время начала выполнения'),
    )
    end_date = models.DateTimeField(
        verbose_name=_('Дата и время завершения выполнения'),
    )

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def __str__(self) -> str:
        return f'{self.service.name}: {self.customer_car.car.brand} {self.customer_car.car.model}'
