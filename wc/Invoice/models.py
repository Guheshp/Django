from django.db import models
from django.utils import timezone
from venue.models import Venue
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
# Create your models here.

class Date(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.date}"

class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    dates = models.ManyToManyField(Date, related_name='enquiries_dates')

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Invoice(models.Model):
    venue = models.ForeignKey(Venue, on_delete= models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    invoice_number = models.CharField(max_length=50,  unique=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    total_amt= models.FloatField(max_length=10)
    pay_amt = models.FloatField(max_length=10)
    balance_amt = models.FloatField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} and {self.venue}"
    