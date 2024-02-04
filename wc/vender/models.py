from django.db import models

# Create your models here.
class Vendor(models.Model):
    company_name = models.CharField(max_length=100)
    vender_name =models.CharField(max_length=100, null=True)
    vender_phone = models.CharField(max_length=12, null=True)
    vender_about = models.CharField(max_length=500, null=True, blank=True)
    Vender_image = models.ImageField(default='defaultvenderimg.png', null=True)
    vender_email = models.EmailField(max_length=200, null=True)
    vender_address = models.CharField(max_length=500,null=True, blank=True)
    vender_city = models.CharField(max_length=200, null=True)
    vender_state = models.CharField(max_length=200, null=True)
    vender_zip = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.vender_name}'s company is {self.company_name}"