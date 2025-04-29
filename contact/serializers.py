from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.

    This serializer handles the validation and serialization of
    contact request data, allowing for the conversion between
    Contact instances and JSON data.

    Attributes:
        name (CharField): The name of the contact.
        email (EmailField): The email address of the contact.
        message (CharField): The message left by the contact.

    Example usage:
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
    """
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')
