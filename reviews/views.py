from django.shortcuts import render
from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly

class ReviewList(generics.ListCreateAPIView):
    """
    API view to list and create reviews.

    This view allows authenticated users to list all reviews or create a new review
    associated with a specific company. On creating a review, the current authenticated user 
    will be automatically set as the owner of the review.

    Attributes:
        queryset (QuerySet): The collection of review instances to be displayed or created.
        serializer_class (class): The serializer used to validate and convert review data.
        permission_classes (list): A list of permission classes that restrict access to authenticated users only.

    Methods:
        perform_create(serializer): Overrides the default create method to assign the current user to the review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific review.

    This view allows users to access, edit, or delete a review based on its ID. 
    Update and delete actions are restricted to the owner of the review or admins.

    Attributes:
        queryset (QuerySet): The collection of review instances to be accessed.
        serializer_class (class): The serializer used to validate and convert review data.
        permission_classes (list): A list of permission classes that restrict access to the owner or admin users.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]