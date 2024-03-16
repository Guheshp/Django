from django.contrib import admin
from .models import Enquiry, Date
# Register your models here.

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number']
    # ordering = ('-name')
    search_fields = ('name','phone_number')

admin.site.register(Date)



