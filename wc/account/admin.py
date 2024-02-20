from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Contact
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "phone", "profile_Image", "is_staff", "is_active","is_superuser",'is_vendor','is_customer', 'last_login', 'date_joined')
    list_filter = ("email", "is_staff", "is_active",'is_vendor','is_customer') 
    fieldsets = (
        (None, {"fields": ("email","phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_superuser",'is_vendor','is_customer', "groups", "user_permissions")}),
      
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email","name","phone", "password1", "password2", "profile_Image", "is_staff",
                "is_active","is_superuser",'is_vendor','is_customer',  "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Contact)

