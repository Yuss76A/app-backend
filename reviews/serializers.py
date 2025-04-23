from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Converts Review instances to/from JSON format for API communication and
    validates the rating. Includes user's full name for display purposes.

    Attributes:
        user_full_name (CharField): The full name of the user who created the review
        Meta (class): Metadata for the serializer, including fields and read-only fields

    Methods:
        validate_rating(value): Ensures that the rating is between 1 and 5.
        Raises a `ValidationError` if outside this range.

    Example usage:
        To create a new review:
        ```python
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
        ```
    """
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_full_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at', 'user_full_name',]

    def validate_rating(self, value):
        """Ensure the rating is between 0 and 5."""
        if value < 0 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 0 and 5."
            )
        return value
