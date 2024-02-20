from django.db import models

from django.db.models import Avg


from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Create your models here.
class Service(models.Model):
    SERIVCES = (
        ('Catering', 'Catering'),
        ('Decor', 'Decor'),
        ('Photography and Videography', 'Photography and Videography'),
        ('Wedding Planning', 'Wedding Planning'),
        ('Makeup and Mehndi', 'Makeup and Mehndi'),
        ('Band Baja', 'Band Baja'),
        ('Artist Management', 'Artist Management'),
        ('Guest Management', 'Guest Management'),
        ('Transport and Logistics', 'Transport and Logistics'),
        ('Entertainment', 'Entertainment'),
    )
    service_name = models.CharField(max_length=200, null=True, choices=SERIVCES)

    def __str__(self):
        return self.service_name
    


class Vendor(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vender_profile')
    services = models.ManyToManyField(Service)
    company_name = models.CharField(max_length=100)
    vender_name =models.CharField(max_length=100, null=True)
    vender_phone = models.CharField(max_length=12, null=True)
    vender_about = models.TextField(null=True, blank=True)
    Vender_image = models.ImageField(default='defaultvenderimg.png', null=True, blank=True)
    vender_email = models.EmailField(max_length=200, null=True)
    vender_address = models.CharField(max_length=500,null=True, blank=True)
    vender_city = models.CharField(max_length=200, null=True)
    vender_state = models.CharField(max_length=200, null=True)
    vender_zip = models.IntegerField(null=True)

    def AveragReview(self):
        review = ReviewVender.objects.filter(vendor=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if review['average'] is not None:
            avg = float(review["average"])
        return avg

    def __str__(self):
        return f"{self.vender_name}'s company is {self.company_name}"
    

class ServiceImage(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images', null=True)
    start_price = models.FloatField(null=True)

    def __str__(self):
        return f"${self.vendor.vender_name}, Image for {self.service.service_name}"

class ReviewVender(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    status = models.BooleanField(default=True)

   
    def __str__(self):
        return self.review  
    


