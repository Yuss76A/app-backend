from django.db import models


class Contact(models.Model):
    """
    Model representing a contact request.

    This model stores information submitted by users through the 
    contact form, including their name, email address, message, 
    and the timestamp when the contact request was created.

    Attributes:
        name (str): The name of the contact.
        email (str): The email address of the contact.
        message (str): The message left by the contact.
        created_at (datetime): The timestamp when the contact request was created.

    Methods:
        __str__(): Returns the name of the contact as a string representation of the model.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
