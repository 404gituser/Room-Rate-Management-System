from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.RoomRate)
admin.site.register(models.OverriddenRoomRate)
admin.site.register(models.DiscountRoomRate)


