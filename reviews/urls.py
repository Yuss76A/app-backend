"""
This is where we set up the URL routes for reviews.
- The first route (empty string) handles listing all reviews and creating new
ones.
- The second route (with <int:pk>) handles viewing, updating, or deleting a
specific review by its ID.
"""
from django.urls import path
from .views import ReviewList, ReviewDetail


urlpatterns = [
    path('', ReviewList.as_view(), name='review-list'),
    path('<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
