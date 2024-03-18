from django.contrib import admin
from .models import Enquiry, Date, CopulesDetails
# Register your models here.

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number']
    # ordering = ('-name')
    search_fields = ('name','phone_number')

admin.site.register(Date)

@admin.register(CopulesDetails)
class CopulesDetailsAdmin(admin.ModelAdmin):

    list_display = ['groomname','bridename','advance_amt', 'created_at','updated_at']
    list_filter = ('groomname', 'bridename')
    ordering = ('-created_at',)



