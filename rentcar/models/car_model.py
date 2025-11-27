from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    oil = models.CharField(max_length=50)
    transmission = models.IntegerField(choices=[(1, "Manual"), (2, "Automatic")])
    seats = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    discount_percent = models.IntegerField(null=True, blank=True)

    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.discount_percent is None:
            return self.price_per_day
        return self.price_per_day - (self.price_per_day * self.discount_percent / 100)
