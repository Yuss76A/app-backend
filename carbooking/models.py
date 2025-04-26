from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError


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

    CURRENCY_TYPES = [
        ('EUR', 'EUR'),
    ]

    name = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=100, choices=CAR_TYPES)
    price_per_day = models.IntegerField(default=50)
    currency = models.CharField(default="EUR", max_length=10, choices=CURRENCY_TYPES)
    max_capacity = models.IntegerField(default=1)
    description = models.TextField(max_length=1000)

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
    image = CloudinaryField("image")
    caption = models.CharField(max_length=255, blank=True, null=True)
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.car.name} - {self.caption or 'No Caption'}"


class BookedDate(models.Model):
    """
    Represents a booking of a car by a user in the rental car application.

    Attributes:
        car (ForeignKey): A reference to the associated Car model, indicating which car is booked.
        user (ForeignKey): A reference to the User model, indicating which user made the booking.
        start_date (DateField): The start date of the booking period.
        end_date (DateField): The end date of the booking period.
        reservation_number (CharField): Unique identifier for the booking.

    Methods:
        __str__(): Returns a string representation of the BookedDate instance.
        clean(): Validates booking dates and checks for overlaps.
        generate_reservation_number(): Creates a unique reservation code.
        save(): Handles reservation number generation and validation before saving.
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='booked_dates')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_bookings')
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reservation_number = models.CharField(max_length=8, unique=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['car', 'start_date', 'end_date'],
                name='unique_booking_for_car_and_dates'
            )
        ]

    def __str__(self):
        return f"Reservation #{self.reservation_number} - {self.car.name} ({self.start_date} to {self.end_date})"

    def clean(self):
        # Ensure the start date is less than or equal to the end date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

        # Ensure no overlapping bookings exist for the same car
        overlapping = BookedDate.objects.filter(
            car=self.car,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).exclude(pk=self.pk if self.pk else None)

        if overlapping.exists():
            raise ValidationError("This car is already booked for some of these dates.")

    def generate_reservation_number(self):
        """Generates a unique 6-character alphanumeric reservation code"""
        import random
        import string
        while True:
            letters = random.choices(string.ascii_uppercase, k=3)
            numbers = random.choices(string.digits, k=3)
            code = ''.join(letters + numbers)
            if not BookedDate.objects.filter(reservation_number=code).exists():
                return code

    def save(self, *args, **kwargs):
        """Override save to generate reservation number and validate before saving"""
        if not self.reservation_number:
            self.reservation_number = self.generate_reservation_number()
        self.full_clean()
        super().save(*args, **kwargs)


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
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, default="")

    # Set unique related names for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
