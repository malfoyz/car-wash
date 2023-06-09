from django.contrib.auth.models import Group
from rest_framework import serializers

from apps.main.models import (
    Brand, Car, CustomerCar, Order,
    Service, ServiceCategory,
)
from apps.users.models import CustomUser


class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор для модели марки"""

    class Meta:
        model = Brand
        fields = ('id', 'name',)


class CarGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели машины"""

    brand = BrandSerializer()

    class Meta:
        model = Car
        fields = ('id', 'brand', 'model')


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для модели машины"""

    class Meta:
        model = Car
        fields = ('id', 'brand', 'model')


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории услуг"""

    class Meta:
        model = ServiceCategory
        fields = ('id', 'name',)


class ServiceGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели услуги"""

    service_category = ServiceCategorySerializer(read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'service_category', 'name', 'price',)


class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели услуги"""

    class Meta:
        model = Service
        fields = ('id', 'service_category', 'name', 'price',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели группы"""

    class Meta:
        model = Group
        fields = ('id', 'name',)


class CustomUserGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'patronymic',
                  'email', 'is_send_notify', 'groups',)


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'patronymic',
                  'email', 'is_send_notify')


class CustomUserWithGroupsGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'patronymic',
                  'email', 'is_send_notify', 'groups',)


class CustomUserWithGroupsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'patronymic',
                  'email', 'is_send_notify', 'groups',)


class CustomUserCutSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'email',)


class CustomerCarGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели машины клиента"""

    car = CarGetSerializer(read_only=True)
    customer = CustomUserCutSerializer(read_only=True)

    class Meta:
        model = CustomerCar
        fields = ('id', 'car', 'customer', 'year', 'number', 'image',)


class CustomerCarSerializer(serializers.ModelSerializer):
    """Сериализатор для модели машины клиента"""

    class Meta:
        model = CustomerCar
        fields = ('id', 'car', 'customer', 'year', 'number', 'image',)

    def validate_customer(self, value):
        """
        Проверяет, что клиент действительно относится к группе клиентов.
        """
        if not value.groups.filter(name='Клиент').exists():
            raise serializers.ValidationError('Выбранный клиент не является клиентом на самом деле')
        return value


class OrderGetSerializer(serializers.ModelSerializer):
    """Сериализатор для модели заказа"""

    service = ServiceGetSerializer()
    customer_car = CustomerCarGetSerializer()
    employee = CustomUserWithGroupsGetSerializer()
    administrator = CustomUserWithGroupsGetSerializer()

    class Meta:
        model = Order
        fields = ('id', 'service', 'customer_car', 'employee',
                  'administrator', 'status', 'start_date', 'end_date',)


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели заказа"""

    class Meta:
        model = Order
        fields = ('id', 'service', 'customer_car', 'employee',
                  'administrator', 'status', 'start_date', 'end_date',)

    def validate_employee(self, value):
        """
        Проверяет, что клиент действительно относится к группе клиентов.
        """
        if not value.groups.filter(name='Работник').exists():
            raise serializers.ValidationError('Выбранный работник не является работником на самом деле')
        return value

    def validate_administrator(self, value):
        """
        Проверяет, что клиент действительно относится к группе клиентов.
        """
        if not value.groups.filter(name='Администратор').exists():
            raise serializers.ValidationError('Выбранный администратор не является администратором на самом деле')
        return value
