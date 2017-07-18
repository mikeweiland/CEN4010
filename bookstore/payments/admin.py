from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.CreditCard)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.FutureOrder)
admin.site.register(models.FutureOrderItem)


