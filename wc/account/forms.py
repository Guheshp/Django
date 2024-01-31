from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class createUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password1', 'password2']
