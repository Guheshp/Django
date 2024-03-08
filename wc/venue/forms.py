from django import forms

from .models import Venue, Event, Booking, CancelVenue, Amenities


class VenueInfoForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'capacity', 'note', 'description','price', 'photo']

class UpdateVenueInfoForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'capacity', 'note', 'description','price', 'photo']
    

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
