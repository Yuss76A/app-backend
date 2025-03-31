from django.urls import path
from .views import ReviewList, ReviewDetail

urlpatterns = [
    path('', ReviewList.as_view(), name='review-list'),  # List all reviews
    path('<int:pk>/', ReviewDetail.as_view(), name='review-detail'),  # Access specific review
]