from django.contrib import admin

# Register your models here.

from .models import( Venue,
                    Booking,
                    Event,
                    VenueImage,
                    Amenities,
                    Restrictions,
                    CancelVenue,
                    ServiceCategory,
                    Service,
                    ContactInformation)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name','user','price','city','state','capacity']
    ordering = ('-name',)
    search_fields = ('name', 'city')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # fields = (('name','venue'), 'date')
    list_display = ['venue','user', 'name','date']
    list_filter = ('date', 'venue')
    ordering = ('-date',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['venue', 'event', 'user', 'booking_type']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['venue','get_category_names','max_capacity','outdoor', 'indoor', 'max_capacity_outdoor', 'max_capacity_indoor']

@admin.register(Restrictions)
class RestrictionsAdmin(admin.ModelAdmin):
    list_display = ['user','venue','restriction_name']


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['user','email', 'phone_number']



admin.site.register(VenueImage)

# admin.site.register(Amenities)

@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ['user','venue', 'amenity_name']

admin.site.register(ServiceCategory)
# admin.site.register(VenueAmenities)
# admin.site.register(VenueRestrictions)

admin.site.register(CancelVenue)