import random
from django.db import models
from django.utils import timezone
from venue.models import Venue

from .utils import generate_invoice_number
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
    

class CopulesDetails(models.Model):
    venue = models.ForeignKey(Venue, on_delete = models.CASCADE, null=True)
    enquiry = models.ForeignKey(Enquiry, on_delete = models.CASCADE, null=True)
    groomname = models.CharField(max_length=255)
    groomDOB = models.DateField(auto_now=False, auto_now_add=False, null=True)
    groomfathername = models.CharField(max_length=255)
    groommothername = models.CharField(max_length=255)
    groom_proof_image = models.ImageField(upload_to="groom_proof_images")
    bridename = models.CharField(max_length=255)
    brideDOB = models.DateField(auto_now=False, auto_now_add=False, null=True)
    bridfathername = models.CharField(max_length=255)
    bridmothername = models.CharField(max_length=255)
    brid_proof_image = models.ImageField(upload_to="brid_proof_images")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "CopulesDetails"  
        verbose_name_plural = "CopulesDetails" 

    def __str__(self):
        return f"{self.groomname} and {self.bridename}"


class Invoice(models.Model):

    TYPE = (
        ("Cash","Cash"),
        ("Online Payment", "Online Payment")
    )
    
    venue = models.ForeignKey(Venue, on_delete= models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    enquiry = models.ForeignKey(Enquiry, on_delete= models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=50,  unique=True,  blank=True)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    advance_amt = models.FloatField( null=True)
    advance_paid_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    payment_type = models.CharField(max_length=200, null=True, choices=TYPE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.enquiry} and {self.venue}"
    
    #generate invoice number
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = generate_invoice_number()
        super().save(*args, **kwargs)

    @property
    def get_balance(self):
        balance = self.venue.price - self.advance_amt
        return balance
    
    def update_advance_amount(self, new_amount, user):
        old_amount = self.advance_amt
        self.advance_amt = new_amount
        self.save()
        InvoiceHistory.objects.create(
            invoice=self,
            user=user,
            old_amount=old_amount,
            new_amount=new_amount,
        )


class InvoiceHistory(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    old_amount = models.FloatField()
    new_amount = models.FloatField()
    date_updated = models.DateTimeField(default=timezone.now)


# class PaymentHistory(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     amount_paid = models.FloatField()
#     payment_date = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"Payment of {self.amount_paid} for Invoice {self.invoice.id} on {self.payment_date}"
    