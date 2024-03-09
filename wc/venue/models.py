from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Create your models here.

class Venue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    address_line_1 = models.CharField(max_length=255, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=6, null=True) 
    capacity = models.IntegerField(default=0)
    note = models.TextField(null=True)
    description = models.TextField(null=True)
    price = models.FloatField(default=0)
    photo = models.ImageField(upload_to='Venueprofiles', null=True)

    def __str__(self):
        return self.name
    
class Amenities(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True)
    amenity_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} amenities are {self.amenity_name}"
    

class Restrictions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True )
    restriction_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user} restriction are {self.restriction_name}"

class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,  related_name='image')
    image = models.ImageField(upload_to='venue-images/')

class ContactInformation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to user account
    venue = models.ForeignKey(Venue, on_delete = models.CASCADE, null=True)
    email = models.EmailField(unique=True)  # Unique email for contact
    phone_number = PhoneNumberField()

    def __str__(self):
        return self.email  # Display email in admin panel
    
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name 
    
class Service(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    category = models.ManyToManyField(ServiceCategory)
    max_capacity = models.IntegerField(default=0)
    outdoor = models.BooleanField(default=False)
    max_capacity_outdoor = models.IntegerField(default=0)
    indoor = models.BooleanField(default=False)
    max_capacity_indoor = models.IntegerField(default=0)

    def get_category_names(self):
        return " / ".join([str(category) for category in self.category.all()])

    get_category_names.short_description = "Categories"

    def __str__(self):
        return self.get_category_names() 

class Event(models.Model):
    venue = models.ForeignKey(Venue, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser,null=True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} in {self.venue}"
    
class Booking(models.Model):
    venue = models.ForeignKey(Venue, on_delete = models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    # quantity = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    booking_type = models.CharField(max_length=100, choices=(('pre paid' , 'pre paid'), ('post paid' , 'post paid')), null=True)

    def __str__(self):
        return f"{self.user} - {self.event.name}"
    
class CancelVenue(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    reason = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.venue} for reason {self.reason}"

 





