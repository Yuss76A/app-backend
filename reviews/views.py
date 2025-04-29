from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from .pagination import StandardResultsPagination


class ReviewList(generics.ListCreateAPIView):
    """
    API view to list and create reviews.

    This view allows authenticated users to:
    - List paginated reviews (8 per page by default)
    - Create new reviews
    - Sort by creation date (newest first by default)
    - Filter by rating (via query parameters)

    On creating a review, the current authenticated user will be automatically
    set as the owner of the review.

    Attributes:
        queryset (QuerySet): The base collection of review instances.
        serializer_class (class): The serializer for review data conversion.
        permission_classes (list): Authenticated users can modify,
        unauthenticated can view.
        pagination_class (class): Custom pagination configuration.
        filter_backends (list): Enabled filtering backends.
        ordering_fields (list): Fields available for ordering.
        ordering (list): Default ordering (-created_at for newest first).

    Methods:
        perform_create(serializer): Assigns current user to new reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Automatically associate the current user with new reviews."""
        serializer.save(user=self.request.user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific review.

    Provides detailed operations on individual reviews:
    - GET: Retrieve full review details
    - PUT/PATCH: Update review (owner only)
    - DELETE: Remove review (owner only)

    Implements owner-only modifications through IsOwnerOrReadOnly permission.

    Attributes:
        queryset (QuerySet): The base collection of review instances.
        serializer_class (class): The serializer for review data conversion.
        permission_classes (list): Restricts modifications to review owner.
        lookup_field (str): Field used for object lookup (default 'pk').

    Note:
        All users can read any review, but only owners can modify/delete.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
