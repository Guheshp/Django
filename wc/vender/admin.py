from django.contrib import admin
from .models import Vendor,Service, ReviewVender, ServiceDetails
# Register your models here.
admin.site.register(Vendor)
admin.site.register(Service)
admin.site.register(ReviewVender)
admin.site.register(ServiceDetails)


