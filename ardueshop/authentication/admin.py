from django.contrib import admin
from .models import ArduUser

# Register your models here.

class ArduUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username", "email", "address", "postal_code")
    search_fields = ("user__first_name", "user__last_name", "user__username", "user__email", "address", "postal_code")

    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = 'Last Name'

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

admin.site.register(ArduUser, ArduUserAdmin)