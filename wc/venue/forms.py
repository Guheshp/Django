from django import forms

from .models import Venue, Event, Booking

class VenueAddForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'capacity', 'phone_number', 'address', 'city', 'state', 'zipcode']
    