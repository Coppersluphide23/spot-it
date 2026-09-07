from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='cars/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'car name: {self.name} price: {self.price}'


class Payment(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    merchant_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'number is {self.phone_number} amount {self.amount}'
