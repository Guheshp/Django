from django import forms
from django.utils import timezone

from .models import (Enquiry,
                    CopulesDetails,
                    Invoice
                    )

class UpdateEnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone_number', 'dates']

class CouplesdetailsForm(forms.ModelForm):
    class Meta:
        model = CopulesDetails
        fields = ['groomname', 'groomDOB', 'groomfathername', 'groommothername', 'groom_proof_image', 'bridename', 'brideDOB', 'bridfathername', 'bridmothername', 'brid_proof_image']

class UpdateCouplesdetailsForm(forms.ModelForm):
    class Meta:
        model = CopulesDetails
        fields = ['groomname', 'groomDOB', 'groomfathername', 'groommothername', 'groom_proof_image', 'bridename', 'brideDOB', 'bridfathername', 'bridmothername', 'brid_proof_image']

class VenuePatmentForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number','advance_amt', 'advance_paid_date', 'payment_type', 'status']


class UpdatePaymentForm(forms.ModelForm):

    paying_amount = forms.FloatField(label='Paying Amount')
    class Meta:
        model = Invoice
        fields = ['invoice_number','advance_paid_date', 'payment_type']

    def __init__(self, *args, **kwargs):
        super(UpdatePaymentForm, self).__init__(*args, **kwargs)
