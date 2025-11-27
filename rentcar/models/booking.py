from django.db import models
from django.contrib.auth.models import User

from rentcar.models.car_model import Car


class Booking(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("card", "Credit Card"),
        ("paypal", "PayPal"),
        ("crypto", "Crypto"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    credit_card_number = models.CharField(max_length=16, null=True, blank=True)
    cvv = models.CharField(max_length=4, null=True, blank=True)
    crypto = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    # Payment
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default="card"
    )
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )

    # Pickup & Dropoff
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    pickup_address = models.CharField(max_length=255, null=True, blank=True)

    dropoff_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)
    dropoff_address = models.CharField(max_length=255, null=True, blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.car.name}"
