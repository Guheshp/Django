from django import forms

from .models import (Enquiry,CopulesDetails
                    )

class UpdateEnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone_number', 'dates']

class CouplesdetailsForm(forms.ModelForm):
    class Meta:
        model = CopulesDetails
        fields = ['groomname', 'groomDOB', 'groomfathername', 'groommothername', 'groom_proof_image', 'bridename', 'brideDOB', 'bridfathername', 'bridmothername', 'brid_proof_image', 'advance_amt', 'advance_paid_date']