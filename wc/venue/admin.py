from django.contrib import admin

# Register your models here.

from .models import Venue, Booking, Event, VenueImage

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']
    ordering = ('-name',)
    search_fields = ('name', 'city')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # fields = (('name','venue'), 'date')
    list_display = ['venue','name','date']
    list_filter = ('date', 'venue')
    ordering = ('-date',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['event', 'user']

admin.site.register(VenueImage)