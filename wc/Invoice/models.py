import random
from django.db import models
from django.utils import timezone
from venue.models import Venue

from django.db.models import Sum

from .utils import generate_invoice_number
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
# Create your models here.

class Date(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.date}"

class Enquiry(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='enquiries', null=True)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=200, null=True)
    dates = models.ManyToManyField(Date, related_name='enquiries_dates')

    def __str__(self):
        return f"{self.name} venue is {self.venue}"
    

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
        # ("Cash","Cash"),
        # ("Online Payment", "Online Payment")
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ("Online Payment", "Online Payment")
    )
    
    venue = models.ForeignKey(Venue, on_delete= models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    enquiry = models.ForeignKey(Enquiry, on_delete= models.CASCADE, null=True)
    invoice_number = models.CharField(max_length=50,  unique=True,  blank=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    advance_amt = models.FloatField( null=True)
    tax_rate = models.FloatField( null=True) 
    new_amt = models.FloatField( null=True)
    advance_paid_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    payment_type = models.CharField(max_length=200, null=True, choices=TYPE)
    status = models.BooleanField(default=False)
    total_amount = models.FloatField(default=0, null=True)
    balance = models.FloatField(default=0, null=True)
    total_paid_amount = models.FloatField(default=0, null=True)

    def __str__(self):
        return f"{self.enquiry} and {self.venue}"
    
    #generate invoice number
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = generate_invoice_number()

        if not self.total_amount:
            self.total_amount = self.venue.price 

        super().save(*args, **kwargs)


    @property
    def get_balance(self):
        get_grand_total = self.Grand_total_amt()
        balance = self.venue.price - get_grand_total
        if balance == 0:
            self.status = True
            # self.advance_amt = self.venue.price
        return balance

    
    def advance_amount(self):
        """
        Calculate the total advance amount paid for this invoice.
        """
        if self.advance_amt is not None:
            return self.advance_amt
        
        return 0

    # def total_paid_amount(self):
    #     if self.pk:  # Check if the instance has been saved/
    #         total_paid = self.invoicehistory_set.aggregate(total_paid=Sum('paying_amount'))['total_paid']
    #         if total_paid is None:
    #             total_paid = 0
    #         if self.advance_amt is not None:
    #             total_paid += self.advance_amt
    #         # Ensure total paid does not exceed the venue price
    #         total_paid = min(total_paid, self.venue.price)
    #         return total_paid
    #     return 0 

    def total_paid_amount(self):
        if self.pk:  # Check if the instance has been saved
            total_paid = self.invoicehistory_set.aggregate(total_paid=Sum('paying_amount'))['total_paid']
            if total_paid is None:
                total_paid = 0
            # Ensure total paid does not exceed the venue price
            total_paid = min(total_paid, self.venue.price)
            return total_paid
        return 0  #
    
    def Grand_total_amt(self):
        """
        Calculate the grand total amount paid for this invoice including the advance amount.
        """
        total_paid = self.total_paid_amount()
        advance_amount = self.advance_amount()
        return total_paid + advance_amount
    
    def tax_payed(self):
        tax = self.new_amt - self.advance_amt
        return tax


class InvoiceHistory(models.Model):
    TYPE = (
        # ("Cash","Cash"),
        # ("Online Payment", "Online Payment")
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ("Online Payment", "Online Payment")
    )
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    new_amount = models.FloatField()
    paying_amount = models.FloatField(null=True)
    date_updated = models.DateTimeField(default=timezone.now)
    payment_type = models.CharField(max_length=200, null=True, choices=TYPE)

   
    def tax_payed(self):
        tax = self.new_amount - self.paying_amount
        return tax
    


    