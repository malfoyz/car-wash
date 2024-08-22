from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import viewsets, generics
from rest_framework.response import Response

from apps.main.models import (
    Brand, Car, CustomerCar, Order, Service, ServiceCategory,
)
from api.auth.permissions import IsAdministrator, IsAdministratorOrReadOnly
from apps.users.models import CustomUser

from .filters import (
    BrandFilter, CarFilter, GroupFilter, OrderFilter, ServiceCategoryFilter,
    ServiceFilter, CustomerCarFilter, CustomUserFilter,
)
from .serializers import (
    BrandSerializer, CarGetSerializer, CarSerializer, GroupSerializer,
    OrderGetSerializer, OrderSerializer, ServiceCategorySerializer,
    ServiceGetSerializer, ServiceSerializer, CustomerCarGetSerializer,
    CustomerCarSerializer, CustomUserGetSerializer, CustomUserWithGroupsSerializer,
    CustomUserSerializer,
)


class BrandViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с марками машин"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filterset_class = BrandFilter
    ordering_fields = ('name',)
    permission_classes = (IsAdministrator,)


class CarViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с машинами"""
    queryset = Car.objects.all()
    filterset_class = CarFilter
    ordering_fields = ('model',)
    permission_classes = (IsAdministrator,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CarGetSerializer

        return CarSerializer


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с категориями услуг"""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    filterset_class = ServiceCategoryFilter
    ordering_fields = ('name',)
    permission_classes = (IsAdministrator,)


class ServiceViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с услугами"""
    queryset = Service.objects.all()
    filterset_class = ServiceFilter
    ordering_fields = ('name', 'price',)
    permission_classes = (IsAdministrator,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ServiceGetSerializer

        return ServiceSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с ролями"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_class = GroupFilter
    ordering_fields = ('name',)
    permission_classes = (IsAdministrator,)


class CustomUserViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с пользователями"""
    queryset = CustomUser.objects.all()
    filterset_class = CustomUserFilter
    ordering_fields = ('first_name', 'last_name', 'patronymic')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CustomUserGetSerializer
        if self.request.user.groups.filter(name='Администратор').exists():
            return CustomUserWithGroupsSerializer
        return CustomUserSerializer


class CustomerCarViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с машинами клиентов"""
    queryset = CustomerCar.objects.all()
    filterset_class = CustomerCarFilter
    ordering_fields = ('year', 'number',)
    permission_classes = (IsAdministrator,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CustomerCarGetSerializer

        return CustomerCarSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """API-ендпоинт для работы с заказами"""
    filterset_class = OrderFilter
    ordering_fields = ('start_date', 'end_date',)
    permission_classes = (IsAdministratorOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderGetSerializer

        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Администратор').exists():
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(Q(employee=user) | Q(customer_car__customer=user))
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Если статус заказа изменен на 1, отправляем сообщение на почту клиента
        if instance.status != serializer.validated_data['status'] and \
           serializer.validated_data['status'] == 1 and \
           instance.customer_car.customer.is_send_notify:
            send_mail(
                subject=f'Статус вашего заказа №{instance.pk} изменен',
                message='Ваш заказ выполнен.',
                from_email='mufasa133@yandex.ru',
                recipient_list=[instance.customer_car.customer.email],
            )

        self.perform_update(serializer)
        return Response(serializer.data)
