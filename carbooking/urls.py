"""
URL configuration for the API endpoints.

This module defines the URL patterns for the API, including endpoints
for managing cars, booked dates, user accounts, and user authentication.

The following URL patterns are included:

- API root endpoint: '/'
- List and create cars: '/cars/'
- Retrieve, update, or delete a specific car: '/cars/<int:pk>/'
- List and create booked dates: '/booked-dates/'
- Retrieve, update, or delete a specific booked date: '/booked-dates/<int:pk>/'
- List users: '/users/'
- Retrieve a specific user: '/users/<int:pk>/'
- User registration: '/register/'
- User login: '/login/'
"""


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
    path('', api_root, name='api-root'),
    path('cars/', CarList.as_view(), name='car-list'),
    path('cars/<int:pk>/', CarDetail.as_view(), name='car-detail'),
    path('booked-dates/', BookedDateList.as_view(), name='bookeddate-list'),
    path(
        'booked-dates/<int:pk>/',
        BookedDateDetail.as_view(),
        name='bookeddate-detail'
    ),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]
