from django.contrib.auth.models import Group
from django_filters import rest_framework as filters

from apps.main.models import (
    Brand, Car, CustomerCar, Order,
    Service, ServiceCategory,
)
from apps.users.models import CustomUser


class BrandFilter(filters.FilterSet):
    """Фильтр марок"""

    class Meta:
        model = Brand
        fields = {
            'name': ['exact', 'contains', 'icontains', 'startswith', 'istartswith']
        }


class CarFilter(filters.FilterSet):
    """Фильтр машин"""

    brand = filters.ModelMultipleChoiceFilter(
        field_name='brand__name',
        to_field_name='name',
        queryset=Brand.objects.all(),
    )

    class Meta:
        model = Car
        fields = {
            'model': ['exact', 'icontains', 'istartswith'],
        }


class ServiceCategoryFilter(filters.FilterSet):
    """Фильтр категорий услуг"""

    class Meta:
        model = ServiceCategory
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }


class ServiceFilter(filters.FilterSet):
    """Фильтр услуг"""

    service_category = filters.ModelMultipleChoiceFilter(
        field_name='service_category__name',
        to_field_name='name',
        queryset=ServiceCategory.objects.all(),
    )

    class Meta:
        model = Service
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'price': ['exact', 'gt', 'gte', 'lt', 'lte'],
        }


class GroupFilter(filters.FilterSet):
    """Фильтр групп пользователей"""

    class Meta:
        model = Group
        fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }


class CustomUserFilter(filters.FilterSet):
    """Фильтр пользователей"""

    groups = filters.ModelMultipleChoiceFilter(
        field_name='groups__name',
        to_field_name='name',
        queryset=Group.objects.all(),
    )

    class Meta:
        model = CustomUser
        fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'patronymic': ['exact', 'icontains', 'istartswith'],
            'email': ['exact', 'icontains', 'istartswith'],
            'is_send_notify': ['exact'],
        }


class CustomerCarFilter(filters.FilterSet):
    """Фильтр машин клиентов"""

    car = filters.ModelMultipleChoiceFilter(
        field_name='car__id',
        to_field_name='id',
        queryset=Car.objects.all(),
    )
    customer = filters.ModelMultipleChoiceFilter(
        field_name='customer__id',
        to_field_name='id',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = CustomerCar
        fields = {
            'year': ['exact', 'gt', 'gte', 'lt', 'lte'],
            'number': ['exact', 'icontains', 'istartswith'],
        }


class OrderFilter(filters.FilterSet):
    """Фильтр заказов"""

    service = filters.ModelMultipleChoiceFilter(
        field_name='service__id',
        to_field_name='id',
        queryset=Service.objects.all(),
    )
    customer_car = filters.ModelMultipleChoiceFilter(
        field_name='cutomer_car__id',
        to_field_name='id',
        queryset=CustomerCar.objects.all(),
    )
    employee = filters.ModelMultipleChoiceFilter(
        field_name='employee__id',
        to_field_name='id',
        queryset=CustomUser.objects.all(),
    )
    administrator = filters.ModelMultipleChoiceFilter(
        field_name='administrator__id',
        to_field_name='id',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'start_date': ['date', 'year', 'month', 'day', 'week_day', 'range'],
            'end_date': ['date', 'year', 'month', 'day', 'week_day', 'range'],
        }