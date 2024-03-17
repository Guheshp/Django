from django import forms

from .models import (Enquiry,
                    )

class UpdateEnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone_number', 'dates']
