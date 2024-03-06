from django import forms

from .models import Venue, Event, Booking, CancelVenue, amenities

    
class AmenityForm(forms.ModelForm):
    class Meta:
        model = amenities
        fields = ['amenity_name']




class AddEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'description']

class UpdateEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'description']

class CheckAvailabilityForm(forms.Form):
    date = forms.DateField(label='Select Date', widget=forms.DateInput(attrs={'type': 'date'}))


class CancelVenueForm(forms.ModelForm):
    class Meta:
        model = CancelVenue
        fields = ["reason"]
