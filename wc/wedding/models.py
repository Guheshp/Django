from django.db import models

from django.contrib.auth import get_user_model

# Create your models here.
CustomUser = get_user_model()

class Couples(models.Model):
    groomname = models.CharField(max_length=200, null=True)
    bridename = models.CharField(max_length=200, null=True)
    groom_dob = models.DateField(auto_now=False, auto_now_add=False, null=True)
    bride_dob = models.DateField(auto_now=False, auto_now_add=False, null=True)
    Wedding_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    phone_number = models.CharField(max_length=12)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Couples"  
        verbose_name_plural = "Couples" 

    def __str__(self):
        return (f" {self.groomname} and  {self.bridename} on {self.Wedding_date} ")
