from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError


class Car(models.Model):
    """
    This class represents a Car object in the rental car app.

    It has attributes like name, type, price per day, currency, max capacity,
    and a description.
    The car type is chosen from a predefined list, and currently, it only
    supports Euros as currency.

    The __str__ method returns the car's name and type for easy identification.
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

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=CAR_TYPES)
    price_per_day = models.IntegerField(default=50)
    currency = models.CharField(
        default="EUR",
        max_length=10,
        choices=CURRENCY_TYPES
    )
    max_capacity = models.IntegerField(default=1)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name} ({self.type})"


class CarImage(models.Model):
    """
    This class handles images related to cars in the rental app.
    It stores the image itself, which is kept on Cloudinary, plus an optional
    caption for extra info. Each image is linked to a specific
    Car through a foreign key.

    The __str__ method displays the car's name and the caption (if provided)
    to easily identify the image.
    """
    image = CloudinaryField("image")
    caption = models.CharField(max_length=255, blank=True, null=True)
    car = models.ForeignKey(
        Car,
        related_name='images',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Image for {self.car.name} - {self.caption or 'No Caption'}"


class BookedDate(models.Model):
    """
    This class represents a booking made by a user for a car in the rental app.
    It links to the specific car and user, and keeps track of the booking
    period with start and end dates.
    Each booking also has a unique reservation number for identification.

    The __str__ method provides a simple string for the booking, while the
    clean method ensures the dates are valid (including no past dates)
    and don’t overlap with existing bookings.
    The generate_reservation_number creates a unique code, and save handles
    generating that code before saving the record.
    """
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='booked_dates'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='car_bookings'
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reservation_number = models.CharField(
        max_length=8,
        unique=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['car', 'start_date', 'end_date'],
                name='unique_booking_for_car_and_dates'
            )
        ]

    def __str__(self):
        return (
            f"Reservation #{self.reservation_number} - {self.car.name} "
            f"({self.start_date} to {self.end_date})"
        )

    def clean(self):
        if self.start_date is None or self.end_date is None:
            raise ValidationError("Start date and end date must be provided.")
        if self.start_date > self.end_date:
            raise ValidationError("End date must be after start date.")

        today = timezone.now().date()
        if self.start_date < today or self.end_date < today:
            raise ValidationError("Cannot book or modify dates in the past.")

        overlaps = BookedDate.objects.filter(
            car=self.car,
            start_date__lt=self.end_date + timedelta(days=1),
            end_date__gt=self.start_date - timedelta(days=1),
        ).exclude(pk=self.pk if self.pk else None)

        if overlaps.exists():
            raise ValidationError(
                "This car is already booked for some of these dates."
            )

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
        """Override save to generate reservation number and validate before
        saving"""
        if not self.reservation_number:
            self.reservation_number = self.generate_reservation_number()
        self.full_clean()
        super().save(*args, **kwargs)


class User(AbstractUser):
    """
    Custom user model inheriting from Django's AbstractUser.
    I added an email field that must be unique and used as the main login.
    The 'full_name' field stores the user's full name.
    The 'username' field is optional and not used for login.
    When you print a user, it shows their email.
    """
    email = models.EmailField('email address', unique=True)
    full_name = models.CharField('full name', max_length=100, blank=True)
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        unique=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
