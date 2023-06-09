from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .main import views


router = DefaultRouter()
router.register(r'brands', views.BrandViewSet, basename='brand')
router.register(r'cars', views.CarViewSet, basename='car')
router.register(r'service_categories', views.ServiceCategoryViewSet, basename='service_category')
router.register(r'services', views.ServiceViewSet, basename='service')
router.register(r'roles', views.GroupViewSet, basename='role')
router.register(r'users', views.CustomUserViewSet, basename='user')
router.register(r'customer_cars', views.CustomerCarViewSet, basename='customer_car')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
