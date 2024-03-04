from django import forms

from .models import Venue, Event, Booking

class VenueAddForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'capacity','booking_cost', 'phone_number', 'address', 'city', 'state', 'zipcode', 'venue_image']
    
class UpdateVenueForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = ['name', 'capacity','booking_cost', 'phone_number', 'address', 'city', 'state', 'zipcode', 'venue_image']


class AddEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'description']

class CheckAvailabilityForm(forms.Form):
    date = forms.DateField(label='Select Date', widget=forms.DateInput(attrs={'type': 'date'}))