from django.contrib import admin
from .models import ArduUser

# Register your models here.

class ArduUserAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "postal_code", "city")

admin.site.register(ArduUser, ArduUserAdmin)