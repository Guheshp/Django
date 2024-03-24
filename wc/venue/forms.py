from django import forms

from .models import (Venue,
                    Event,
                    Booking, 
                    CancelVenue, 
                    Amenities, 
                    Restrictions, 
                    VenueImage, 
                    ContactInformation, 
                    Service)


class VenueInfoForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name','gst_number','address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'capacity', 'note', 'description','price', 'photo']

class UpdateVenueInfoForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name','gst_number', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'capacity', 'note', 'description','price', 'photo']
    

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

class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = ['email', 'phone_number']
        
class UpdateContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = ['email', 'phone_number']

        
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
