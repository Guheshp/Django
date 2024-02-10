from django.contrib import admin
from .models import Vendor, Image, Service
# Register your models here.
admin.site.register(Vendor)

admin.site.register(Image)
admin.site.register(Service)

