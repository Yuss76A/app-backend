from django.urls import path
from .views import (
    api_root,
    CarList,
    CarDetail,
    BookedDateList,
    BookedDateDetail,
    UserList,
    UserDetail,
    Register,
    Login
)

urlpatterns = [
    path('', api_root, name='api-root'),  # Root URL for the car booking app
    path('cars/', CarList.as_view(), name='car-list'),  # List and create cars
    path('cars/<int:pk>/', CarDetail.as_view(), name='car-detail'),  # Detail, update, delete a specific car
    path('booked-dates/', BookedDateList.as_view(), name='bookeddate-list'),  # List and create booked dates
    path('booked-dates/<int:pk>/', BookedDateDetail.as_view(), name='bookeddate-detail'),  # Detail, update, delete a specific booked date
    path('users/', UserList.as_view(), name='user-list'),  # List users
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),  # Detail of a specific user
    path('register/', Register.as_view(), name='register'),  # User registration
    path('login/', Login.as_view(), name='login'),  # User login
]