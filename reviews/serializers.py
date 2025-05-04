from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for converting Review model instances to and from JSON,
    primarily used in API interactions. It includes a field for the user's
    full name to help display who wrote each review. The serializer also
    performs validation to ensure that the rating is within the valid range
    of 1 to 5, and that comments are not left empty or filled with only
    whitespace. 

    Usage example:
        To create or update a review, instantiate the serializer with
        data and call `is_valid()`. If valid, save the review with the
        user set to the current user.
    """
    user_full_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'user_full_name',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['user', 'created_at', 'user_full_name',]

    def validate_rating(self, value):
        """Ensure the rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value

    def validate_comment(self, value):
        """Ensure comment is not empty."""
        if not value.strip():
            raise serializers.ValidationError(
                "Comment cannot be empty."
            )
        return value
