from django import forms
from django.utils import timezone

from .models import (Enquiry,
                    CopulesDetails,
                    Invoice, 
                    InvoiceHistory
                    )

class UpdateEnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name','email', 'phone_number', 'dates']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

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
        fields = ['invoice_number','advance_amt', 'tax_rate', 'advance_paid_date', 'payment_type', 'status']


class UpdatePaymentForm(forms.ModelForm):

    paying_amount = forms.FloatField(label='Paying Amount')
    class Meta:
        model = Invoice
        fields = ['invoice_number','advance_paid_date', 'payment_type']

    def __init__(self, *args, **kwargs):
        super(UpdatePaymentForm, self).__init__(*args, **kwargs)

class FirstPaymentUpdateform(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ['advance_amt','tax_rate','advance_paid_date','payment_type']


class Invoice_History_Update_Form(forms.ModelForm):
    model = InvoiceHistory
    firlds = ['new_amount', 'paying_amount']