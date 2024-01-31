from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "phone","is_staff", "is_active","is_superuser")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email","phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active","is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email","phone", "password1", "password2", "is_staff",
                "is_active","is_superuser", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)





admin.site.register(CustomUser, CustomUserAdmin)
