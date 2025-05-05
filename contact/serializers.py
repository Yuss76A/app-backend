from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.

    Handles validation to ensure the message isn't empty or just whitespace.
    """
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')

    def validate_message(self, value):
        """Ensure message contains non-whitespace content"""
        if not value.strip():
            raise serializers.ValidationError('Message cannot be empty.')
        return value
