from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from cloudinary.models import CloudinaryField

class Car(models.Model):
    """
    Represents a car available for rent in the rental car application.

    Attributes:
        name (str): The name of the car (e.g., "Toyota Camry").
        type (str): The type of car, selected from predefined choices (sedan, SUV, hatchback, convertible, pickup).
        price_per_day (int): The rental price per day for the car, defaulting to 50 Euros.
        currency (str): The currency in which the price is set, defaulting to Euro (EUR).
        max_capacity (int): The maximum number of passengers that the car can accommodate, defaulting to 1.
        description (str): A detailed description of the car, limited to 1000 characters.

    Choices:
        CAR_TYPES (list): A list of tuples representing valid car types.
        CURRENCY_TYPES (list): A list of tuples representing valid currency types (currently only Euro is supported).

    Methods:
        __str__(): Returns a string representation of the car, including its name and type.
    """
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
    """
    Represents an image associated with a car in the rental car application.

    Attributes:
        image (CloudinaryField): The image file for the car, stored on Cloudinary.
        caption (str, optional): An optional caption for the image, allowing for additional context or description.
        car (ForeignKey): A reference to the associated Car model, indicating which car this image belongs to.

    Methods:
        __str__(): Returns a string representation of the CarImage instance, showing the car's name and the caption (if available).
    """
    image = CloudinaryField("image")  # Image field for the car, stored in Cloudinary
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for the image
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)  # Relationship to the Car model
    
    def __str__(self):
        return f"Image for {self.car.name} - {self.caption or 'No Caption'}"


class BookedDate(models.Model):
    """
    Represents a booking of a car by a user in the rental car application.

    Attributes:
        car (ForeignKey): A reference to the associated Car model, indicating which car is booked.
        user (ForeignKey): A reference to the User model, indicating which user made the booking.
        date (DateField): The date for which the car is booked.

    Methods:
        __str__(): Returns a string representation of the BookedDate instance,
                    showing the booking date, car name, and username of the user.
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='booked_dates')  # Relationship to the Car model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_bookings')  # Relationship to the User model
    date = models.DateField()  # Date the car is booked

    def __str__(self):
        return f"{self.date} - {self.car.name} booked by {self.user.username}"


class User(AbstractUser):
    """
    Represents an extended user model for the rental car application.

    This model extends the default Django AbstractUser model to include additional fields
    that support user registration and management.

    Attributes:
        email (EmailField): A unique email address for the user, which is used for authentication.
        full_name (str): The full name of the user, used to provide a personalized experience.
        groups (ManyToManyField): A many-to-many relationship to groups, allowing the user to belong to multiple groups.
        user_permissions (ManyToManyField): A many-to-many relationship to permissions, granting specific access rights to the user.

    Methods:
        __str__(): Returns a string representation of the User instance, typically the user's username or email.
    """
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