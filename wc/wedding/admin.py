from django.contrib import admin
from .models import Couples

# Register your models here.

class CoupleAdmin(admin.ModelAdmin):
    list_display = ('husband', 'wife')

admin.site.register(Couples)
