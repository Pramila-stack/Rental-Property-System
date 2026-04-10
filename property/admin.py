from django.contrib import admin

from property.models import Booking, Property, Review

# Register your models here.
admin.site.register(Property)
admin.site.register(Review)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'approved')
    list_filter = ('approved',)