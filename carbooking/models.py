from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from cloudinary.models import CloudinaryField

class Car(models.Model):
    # Choices for the type of car
    CAR_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('convertible', 'Convertible'),
        ('pickup', 'Pickup'),
    ]
    
    # Choices for currency type; only Euro is available
    CURRENCY_TYPES = [
        ('EUR', 'EUR'),  # Only Euro
    ]

    name = models.CharField(max_length=100, blank=True, default='')  # Car name
    type = models.CharField(max_length=100, choices=CAR_TYPES)  # Type of the car
    price_per_day = models.IntegerField(default=50)  # Price per day for renting the car
    currency = models.CharField(default="EUR", max_length=10, choices=CURRENCY_TYPES)  # Currency (only Euros)
    max_capacity = models.IntegerField(default=1)  # Maximum number of passengers
    description = models.TextField(max_length=1000)  # Description of the car
    
    def __str__(self):
        return f"{self.name} ({self.type})"
    
class CarImage(models.Model):
    image = CloudinaryField("image")  # Image field for the car, stored in Cloudinary
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for the image
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)  # Relationship to the Car model
    
    def __str__(self):
        return f"Image for {self.car.name} - {self.caption or 'No Caption'}"

class BookedDate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='booked_dates')  # Relationship to the Car model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_bookings')  # Relationship to the User model
    date = models.DateField()  # Date the car is booked

    def __str__(self):
        return f"{self.date} - {self.car.name} booked by {self.user.username}"

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Unique email for the user
    full_name = models.CharField(max_length=100, default="")  # Full name of the user

    # Set unique related names for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Unique related name
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Unique related name
        blank=True,
        help_text='Specific permissions for this user.'
    )