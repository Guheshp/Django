from django import forms

from . models import Couples

class CouplesRegistrtaion(forms.ModelForm):

    class Meta:
        model = Couples
        fields = ['groomname', 'bridename', 'groom_dob', 'bride_dob', 'phone_number', 'Wedding_date']


class CoupleUpdateForm(forms.ModelForm):

    class Meta:
        model = Couples
        fields = ['groomname', 'bridename', 'groom_dob', 'bride_dob', 'phone_number', 'Wedding_date']

