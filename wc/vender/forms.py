from django import forms

from .models import Vendor

class VenderRegistrationForm(forms.ModelForm):

    class Meta:

        model = Vendor
        fields = ['vender_name', 'company_name','Vender_image', 'vender_phone', 'vender_email',
                 'vender_address', 'vender_city', 'vender_state', 'vender_zip' ]
        widgets = {
            'vender_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Vender Name', 'required': True}),
            'company_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Company Name', 'required': True}),
            'vender_phone':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Phone Number', 'required': True}),
            'Vender_image':forms.FileInput(attrs={'class':'form-control', 'placeholder': 'Choose Image', 'required': True}),
            'vender_email':forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter Email', 'required': True}),
            'vender_address':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Address', 'required': True}),
            'vender_about':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'About You', 'required': True}),
            'vender_city':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter City', 'required': True}),
            'vender_state':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter State', 'required': True}),
            'vender_zip':forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter Zipcode', 'required': True}),
        }

class VenderUpdateForm(forms.ModelForm):

    class Meta:

        model = Vendor
        fields = ['vender_name', 'company_name', 'vender_phone', 'Vender_image', 'vender_email',
                 'vender_address', 'vender_city', 'vender_state', 'vender_zip' ]
        widgets = {
            'vender_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Vender Name', 'required': True}),
            'company_name':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Company Name', 'required': True}),
            'vender_phone':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Phone Number', 'required': True}),
            'Vender_image':forms.FileInput(attrs={'class':'form-control', 'placeholder': 'Choose Image', 'required': True}),
            'vender_about':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'About You', 'required': True}),
            'vender_email':forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter Email', 'required': True}),
            'vender_address':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Address', 'required': True}),
            'vender_city':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter City', 'required': True}),
            'vender_state':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter State', 'required': True}),
            'vender_zip':forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter Zipcode', 'required': True}),
        }


