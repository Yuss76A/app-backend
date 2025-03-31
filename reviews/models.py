from django.db import models
from django.conf import settings


class Review(models.Model):
    """
    Represents a review for a car by a user.

    Attributes:
        car (ForeignKey): The car that this review is associated with.
        user (ForeignKey): The user who wrote the review.
        rating (IntegerField): A rating value, typically on a scale (e.g., 1 to 5) indicating the user's satisfaction.
        comment (TextField): The detailed comment or feedback provided by the user regarding the car.
        created_at (DateTimeField): A timestamp that records when the review was created, automatically set when the review is created.

    Methods:
        __str__(): Returns a string representation of the review, indicating the car name and the user's full name.
    """
    car = models.ForeignKey('carbooking.Car', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.car.name} by {self.user.full_name}"
