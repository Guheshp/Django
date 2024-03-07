from django.contrib import admin

# Register your models here.

from .models import( Venue,
                    Booking,
                    Event,
                    VenueImage,
                    amenities,
                    Restrictions,
                    CancelVenue,
                    VenueAmenities,
                    VenueRestrictions,
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

@admin.register(VenueRestrictions)
class VenueRestrictionsAdmin(admin.ModelAdmin):
    list_display = ['venue','get_restrictions_names']

@admin.register(VenueAmenities)
class VenueAmenitiesAdmin(admin.ModelAdmin):
    list_display = ['venue','get_amenitie_names']


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['user','email', 'phone_number']



admin.site.register(VenueImage)
admin.site.register(amenities)
admin.site.register(ServiceCategory)
# admin.site.register(VenueAmenities)
# admin.site.register(VenueRestrictions)
admin.site.register(Restrictions)
admin.site.register(CancelVenue)