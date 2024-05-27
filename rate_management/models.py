from django.db import models

class RoomRate(models.Model):
    room_id = models.IntegerField()
    room_name = models.CharField(max_length=100)
    default_rate = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return f"Room: {self.room_name}, Price: {self.default_rate}"


class OverriddenRoomRate(models.Model):
    room_rate = models.ForeignKey(to=RoomRate, on_delete= models.CASCADE, related_name= 'overrided_rate')
    overridden_rate = models.DecimalField(decimal_places=2, max_digits=10)
    stay_date = models.DateField()

class Discount(models.Model):
    DISCOUNT_CHOICES = {
        "Percentage": "percentage",
        "Fixed": "fixed"
    }

    discount_id = models.IntegerField()
    discount_name = models.CharField(max_length=150)
    discount_type = models.CharField(choices=DISCOUNT_CHOICES, default= "percentage", max_length=10)
    discount_value = models.DecimalField(decimal_places=2, max_digits=10)

class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(to=RoomRate, on_delete= models.CASCADE)
    discount = models.ForeignKey(to=Discount, on_delete= models.CASCADE)

    

