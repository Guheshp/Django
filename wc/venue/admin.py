from django.contrib import admin

# Register your models here.

from .models import Venue, Booking, Event, VenueImage, amenities

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name','user','booking_cost','city','state','capacity']
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

admin.site.register(VenueImage)
admin.site.register(amenities)