from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from rest_framework import viewsets
from .models import CarImage
from .models import User, Car, BookedDate
from .serializers import (
    CarSerializer,
    BookedDateSerializer,
    UserSerializer,
    CarImageSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


# API root endpoint
@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint.

    Provides links to the main API endpoints for cars, users, and booked dates.

    Args:
        request: The HTTP request object.
        format: Optional format argument for response.

    Returns:
        Response: A response with links to the main API endpoints.
    """
    return Response({
        'cars': reverse('car-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'booked-dates': reverse(
            'bookeddate-list',
            request=request,
            format=format
        )
    })


# Car views
class CarList(generics.ListCreateAPIView):
    """
    API view to list and create cars.

    Handles HTTP GET for listing all cars and POST for creating a new car.

    Permissions:
        Admin users can create new cars, others can only read.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific car.

    Handles HTTP GET, PUT, PATCH, and DELETE requests for a car.

    Permissions:
        Admin users have full access; others cannot modify.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookedDateList(generics.ListCreateAPIView):
    """
    API view to list and create booked dates.

    Handles HTTP GET for listing all booked dates and POST for creating a
    new booking.

    Permissions:
        Authenticated users can create bookings; others can only read.
    """
    queryset = BookedDate.objects.all()
    serializer_class = BookedDateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Retrieves the list of booked dates.
        Filters the queryset to only include dates booked by the logged-in
        user if they are not an admin.
        Returns:
            QuerySet: The filtered queryset of booked dates.
        """
        user = self.request.user
        if not user.is_superuser and not user.is_staff:
            return BookedDate.objects.filter(user=user)
        return super().get_queryset()


class BookedDateDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific booked date.

    Handles HTTP GET, PUT, PATCH, and DELETE requests for a booked date.

    Permissions:
        Authenticated users can modify their own bookings; admin users
        have full access.
    """
    queryset = BookedDate.objects.all()
    serializer_class = BookedDateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        """
        Overrides the method to ensure permissions are checked.
        """
        booked_date = super().get_object()
        # The IsOwnerOrReadOnly permission class will handle ownership checks
        return booked_date


# User views
class UserList(generics.ListAPIView):
    """
    API view to list users.

    Handles HTTP GET for listing all users or filtering to show only the
    requesting user.

    Permissions:
        Admin users can see all users; regular users only see their own
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Retrieves the list of users.

        Filters the queryset to return all users for admins and only the
        requesting user for non-admins.

        Returns:
            QuerySet: The filtered queryset of users.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=user.id)


class UserDetail(generics.RetrieveAPIView):
    """
    API view to retrieve a specific user's details.

    Handles HTTP GET requests for user details.

    Permissions:
        Users can view their own details; admins can view any user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """
        Retrieves the user object.

        Allows access based on user roles (self or admin).

        Returns:
            User: The user object to be retrieved.

        Raises:
            PermissionDenied: If the user does not have permission to access
            the details.
        """
        user = self.request.user
        obj = super().get_object()

        # Allow access if the user is fetching their own details or is an admin
        if obj == user or user.is_staff or user.is_superuser:
            return obj
        else:
            raise PermissionDenied(
                "You do not have permission to access this user's details."
            )


# Registration view
class Register(generics.CreateAPIView):
    """
    API view for user registration.

    Allows new users to register, saving their details and generating an
    authentication token.

    Attributes:
        queryset (QuerySet): The queryset containing all User objects.
        serializer_class (Serializer): The serializer class used for user data.

    Methods:
        perform_create(serializer): Saves the new user and generates an
        authentication token.
        create(request, *args, **kwargs): Custom method to return the user
        data and token in the response.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Saves the new user instance and generates an auth token.

        Args:
            serializer (Serializer): The serializer containing validated user
            data.

        Side Effects:
            Creates a new user and associates an authentication token.
        """
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        # Prepare response data
        self.response_data = {
            "user": {
                "id": user.id,
                "username": user.email,
                "email": user.email,
                "full_name": user.full_name
            },
            "token": token.key,
        }

    def create(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to create a user.

        Args:
            request: The request object containing user data.
            *args, **kwargs: Additional arguments.

        Returns:
            Response: A response object containing user data and the
            authentication token.
        """
        super().create(request, *args, **kwargs)
        return Response(self.response_data)


# Login view
class Login(APIView):
    """
    Handles user login by email and password.
    Checks if the user exists and if the password is correct.
    If successful, returns an authentication token along with user info.
    Includes a welcome message in the response on successful login.
    Raises authentication errors if the user is not found or password is
    invalid.
    """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise AuthenticationFailed('Invalid password')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name
            },
            'welcome_message': "Welcome to Happy Rental Jönköping!"
        })


# Test token view
class TestToken(generics.RetrieveAPIView):
    """
    API view to test token authentication.

    Retrieves and displays user details based on the provided token.

    Attributes:
        queryset (QuerySet): The queryset containing all User objects.
        serializer_class (Serializer): The serializer class used for user data.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CarImageViewSet(viewsets.ModelViewSet):
    """
    Manages CRUD operations for car images.

    Allows anyone to view images, but only admins can add, edit, or delete them.
    """
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    permission_classes = [IsAdminOrReadOnly]
