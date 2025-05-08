from rest_framework import serializers
from .models import Car, CarImage, BookedDate, User


class CarImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the CarImage model.

    This serializer handles the conversion of CarImage instances to and from
    JSON.
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
        queryset=User.objects.all(),
        required=False
    )
    reservation_number = serializers.CharField(
        read_only=True,
        help_text="Auto-generated booking reference code"
    )

    class Meta:
        model = BookedDate
        fields = [
            'url',
            'id',
            'car',
            'user',
            'start_date',
            'end_date',
            'reservation_number'
        ]

    def validate(self, attrs):

        car = attrs.get('car', getattr(self.instance, 'car', None))
        start_date = attrs.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )
        end_date = attrs.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
            )

        if not (car and start_date and end_date):
            return attrs

        overlaps = BookedDate.objects.filter(
            car=car,
            start_date__lte=end_date,
            end_date__gte=start_date,
        )
        if self.instance:
            overlaps = overlaps.exclude(pk=self.instance.pk)

        if overlaps.exists():
            raise serializers.ValidationError(
                "This car is already booked for the selected dates."
            )

        return attrs

    def create(self, validated_data):
        """Automatically sets the user from request and handles reservation
        number
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)


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


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Converts User objects to and from JSON, allowing creation with email,
    full name, and password. It hashes the password before saving.
    """
    name = serializers.CharField(source='full_name', write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        user = User(
            email=validated_data['email'],
            full_name=full_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
