from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# Create your models here.

class amenities(models.Model):
    amenity_name = models.CharField(max_length=100)

    def __str__(self):
        return self.amenity_name

class Restrictions(models.Model):
    restriction_name = models.CharField(max_length=100)

    def __str__(self):
        return self.restriction_name

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
    
class VenueAmenities(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,  related_name='amenity_name')
    amenitie = models.ManyToManyField(amenities)

    def get_amenitie_names(self):
        # amenities = "\n".join([str(amenitie) for amenitie in self.amenitie.all()])
        # return amenities
        amenities = []
        for index, amenitie in enumerate(self.amenitie.all(), start=1):
            amenities.append(f"{index}. {amenitie}")
        amenities = "\n".join(amenities)
        return amenities 

    get_amenitie_names.short_description = "amenitie"

    def __str__(self):
       return f"{self.venue} and its amenities:\n{self.get_amenitie_names()}"
    

class VenueRestrictions(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE,  related_name='restrictions_name')
    restrictions = models.ManyToManyField(Restrictions)

    def get_restrictions_names(self):
        # return ", ".join([str(restrictions) for restrictions in self.restrictions.all()])
    
        restrictions_list = []
        for index, restriction in enumerate(self.restrictions.all(), start=1):
            restrictions_list.append(f"{index}. {restriction}")
        restrictions_all = "\n".join(restrictions_list)
        return restrictions_all


    get_restrictions_names.short_description = "restrictions"

    def __str__(self):
        return f"{self.venue} and its amenities {self.restrictions}"


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

 





