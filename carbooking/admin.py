"""
Admin configuration for the Car Booking application.

This module registers the User, Car, BookedDate, and CarImage models
with the Django admin site, allowing for management through the 
admin interface.
"""

from django.contrib import admin
from .models import User, Car, BookedDate, CarImage


admin.site.register(User)
admin.site.register(Car)
admin.site.register(BookedDate)
admin.site.register(CarImage)
