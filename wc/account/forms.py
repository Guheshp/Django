from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from .models import CustomUser

from django import forms

from django.forms.widgets import PasswordInput, TextInput, EmailInput

class createUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [ 'email', 'name','phone', 'password1', 'password2']


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

        password = None

        model = CustomUser
        fields = [ 'email', 'name','phone']

class EditAdminProfilrForm(UserChangeForm):

    class Meta:
        
        password = None

        model = CustomUser
        fields = ['name', 'email', 'phone', 'is_staff', 'is_superuser', 'is_active']