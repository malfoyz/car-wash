from django.contrib import admin

from .models import *


admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(ServiceCategory)
admin.site.register(Service)
admin.site.register(CustomerCar)
admin.site.register(Order)
