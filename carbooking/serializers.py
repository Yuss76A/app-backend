from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Car, CarImage, BookedDate, User


class CarImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the CarImage model.

    This serializer handles the conversion of CarImage instances to and from JSON.
    It includes the associated car's URL and the URL of the image.
    """

    car = serializers.HyperlinkedRelatedField(
        view_name='car-detail',
        queryset=Car.objects.all()
    )
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        """
        Method to retrieve the full URL of the image.

        Args:
            obj: The CarImage instance.

        Returns:
            str: The URL of the image.
        """
        return obj.image.url

    class Meta:
        model = CarImage
        fields = ['id', 'image', 'caption', 'car']


class BookedDateSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the BookedDate model.
    This serializer manages the conversion of BookedDate instances to and from 
    JSON, linking the booking to the respective car and user.
    """
    car = serializers.HyperlinkedRelatedField(
        view_name='car-detail',
        queryset=Car.objects.all()
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )

    class Meta:
        model = BookedDate
        fields = ['url', 'id', 'car', 'user', 'date']


class CarSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Car model.

    This serializer converts Car instances into JSON format,
    including nested details for booked dates and associated images.
    """

    booked_dates = BookedDateSerializer(many=True, read_only=True)
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['url', 'id', 'name', 'type', 'price_per_day', 'currency', 
                  'max_capacity', 'description', 'booked_dates', 'images']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the User model.

    This serializer is used to manage the conversion of User instances to
    and from JSON, including password hashing before saving.
    """

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'full_name']

    def validate_password(self, value):
        """
        Hash the password before saving it.

        Args:
            value: The raw password entered by the user.

        Returns:
            str: The hashed password.
        """
        return make_password(value)
