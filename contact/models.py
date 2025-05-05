from django.db import models
from django.core.exceptions import ValidationError


class Contact(models.Model):
    """
    Handles contact form submissions. Make sure the message actually
    has content.
    When saving, it runs validation to prevent empty messages from
    being stored.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Ensures message contains non-whitespace content"""
        if not self.message.strip():
            raise ValidationError(
                {'message': 'Message must contain actual content.'}
            )
        super().clean()

    def save(self, *args, **kwargs):
        """Always runs validation before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
