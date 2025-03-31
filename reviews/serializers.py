from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    This serializer is used to convert Review instances to JSON format and 
    vice versa for API communication. It automatically handles the inclusion
    of necessary fields in review data, including relationships to car and user.

    Attributes:
        Meta (class): Contains metadata about the serializer.
            - model (class): The model associated with this serializer (Review).
            - fields (list): A list of fields to include in the serialization.
            - read_only_fields (list): A list of fields that should be read-only 
              at the time of creation or update. Typically, the 'user' is set 
              automatically to the authenticated user and 'created_at' is set to 
              the timestamp of creation.

    Example:
        To serialize or deserialize review data, you would create an instance 
        of the serializer with validated data like so:

        serializer = ReviewSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically set the user
    """
    class Meta:
        model = Review
        fields = ['id', 'car', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']