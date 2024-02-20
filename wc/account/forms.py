from django.contrib.auth.forms import (UserCreationForm,
                                        AuthenticationForm,
                                        UserChangeForm,
                                        PasswordChangeForm,
                                        )

from .models import CustomUser, Contact

from django import forms

from django.forms.widgets import PasswordInput, TextInput, EmailInput

class createUserForm(UserCreationForm):

    # profile_image = forms.ImageField(label='Profile Image', required=False) 
    # is_vendor = forms.BooleanField(label='Register as Vendor', required=False)
    is_customer = forms.BooleanField(label='Register as User', required=True)
    
    class Meta:
        model = CustomUser
        fields = [ 'email', 'name','phone','profile_Image', 'password1', 'password2','is_customer']

class CreateUserVenderForm(UserCreationForm):
    is_vendor = forms.BooleanField(label='Register as Vendor', required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone', 'profile_Image', 'password1', 'password2', 'is_vendor']

# class LoginForm(AuthenticationForm):

#     username = forms.EmailField(widget=EmailInput())
#     password = forms.CharField(widget=PasswordInput())

class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        widget = EmailInput(attrs={'class': '', }),
        # label='Email',
        # required=False
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={'class': '', })
    )

class EditUserProfilrForm(UserChangeForm):

    class Meta:
        profile_image = forms.ImageField(label='Profile Image', required=False) 

        password = None

        model = CustomUser
        fields = [ 'email', 'name','phone', 'profile_Image']

    def __init__(self, *args, **kwargs):   
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields['email'].widget.attrs['readonly'] = True

        

class EditAdminProfilrForm(UserChangeForm):

    class Meta:
        
        password = None

        model = CustomUser
        fields = ['name', 'email', 'phone', 'is_staff', 'is_superuser', 'is_active',]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['user_email', 'subject', 'message']