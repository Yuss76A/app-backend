from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Company(models.Model):
    """
    Represents a company in the application.

    This model is used to store information about companies that users can review.

    Attributes:
        name (CharField): The name of the company. This is a required field with a maximum length of 255 characters.
        description (TextField): A brief description of the company. This field is optional and can be left blank.
        address (CharField): The physical address of the company. This optional field has a maximum length of 512 characters.
        website_url (URLField): The company's website URL. This field is also optional and can be left blank.

    Methods:
        __str__(): Returns the name of the company when the object is converted to a string.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Review(models.Model):
    """
    Represents a review for a rental company.

    Attributes:
        company (ForeignKey): The company being reviewed.
        user (ForeignKey): The user who wrote the review.
        rating (IntegerField): Rating from 0 to 5 for the company.
        comment (TextField): Text feedback provided by the user.
        created_at (DateTimeField): Timestamp for when the review was created.

    Methods:
        clean(): Validates that the rating is between 0 and 5.
        save(*args, **kwargs): Overrides save to ensure rating validation before saving.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
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
        return f"Review for {self.company.name} by {self.user.full_name}, Rating: {self.rating}"
