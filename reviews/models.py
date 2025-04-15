from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Review(models.Model):
    """
    Represents a review created by users.

    Attributes:
        user (ForeignKey): The user who wrote the review.
        rating (IntegerField): Rating from 0 to 5 for the review.
        comment (TextField): Text feedback provided by the user.
        created_at (DateTimeField): Timestamp for when the review was created.

    Methods:
        clean(): Validates that the rating is between 0 and 5.
        save(*args, **kwargs): Overrides save to ensure rating validation
        before saving.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate that rating is between 0 and 5."""
        if self.rating < 0 or self.rating > 5:
            raise ValidationError('Rating must be between 0 and 5.')

    def save(self, *args, **kwargs):
        """Override save to validate the rating before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.username}, Rating: {self.rating}"
