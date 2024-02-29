from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Create your models here.

class Venue(models.Model):
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=0, null=0, blank=True)


    def __str__(self):
        return self.name
    
class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='venue-images/')


class Event(models.Model):
    venue = models.ForeignKey(Venue, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser,null=True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} in {self.venue}"
    
class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event.name}"






