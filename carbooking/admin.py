from django.contrib import admin
from .models import User, Car, BookedDate, CarImage


admin.site.register(User)
admin.site.register(Car)
admin.site.register(BookedDate)
admin.site.register(CarImage)
