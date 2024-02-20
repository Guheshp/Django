from django.db import models
from django.contrib.auth.base_user import  BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, phone=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email,  phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password,  phone=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_vendor", True)
        extra_fields.setdefault("is_customer", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_vendor") is not True:
            raise ValueError(_("Superuser must have is_vendor=True."))
        if extra_fields.get("is_customer") is not True:
            raise ValueError(_("Superuser must have is_customer=True."))
        return self.create_user(email, password, phone, **extra_fields)
    

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=12, unique=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    profile_Image = models.ImageField(upload_to='profile_img', null=True, blank=True, default='userdefaultimg.png')
    last_login = models.DateTimeField(_("last login"), auto_now=True, null=True,)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True, null=True,)

    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Contact(models.Model):
    user_email = models.EmailField(max_length=200, null= True)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.user_email




    
    
