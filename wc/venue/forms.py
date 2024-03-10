from django import forms

from .models import Venue, Event, Booking, CancelVenue, Amenities, Restrictions, VenueImage


class VenueInfoForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'capacity', 'note', 'description','price', 'photo']

class UpdateVenueInfoForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'capacity', 'note', 'description','price', 'photo']
    

# class deleteAmenitiesForm(forms.ModelForm):
#     class Meta:
#         model = Amenities
#         fields = ['amenity_name']
         

class UpdateAmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        fields = ['amenity_name']
    
class UpdateRestrictionsForm(forms.ModelForm):
    class Meta:
        model = Restrictions
        fields = ['restriction_name']
    

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = VenueImage
        fields = ['image']

class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = VenueImage
        fields = ['image']
        
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
