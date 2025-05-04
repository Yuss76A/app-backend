from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Review(models.Model):
    """
    Represents a review created by users.

    Attributes:
        user (ForeignKey): The user who wrote the review.
        rating (IntegerField): Rating from 1 to 5 for the review.
        comment (TextField): Text feedback provided by the user
        (cannot be empty).
        created_at (DateTimeField): Timestamp for when the review was created.
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
        """Validate that rating is between 1 and 5 and comment is not empty."""
        if self.rating < 1 or self.rating > 5:
            raise ValidationError({'rating': 'Rating must be between 1 and 5.'})
        if not self.comment.strip():
            raise ValidationError({'comment': 'Comment cannot be empty.'})

    def save(self, *args, **kwargs):
        """Override save to validate before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.username}, Rating: {self.rating}"
