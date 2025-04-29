"""
URL configuration for the contact requests API.

This module defines the URL patterns for handling contact requests,
including the ability to create new contacts, list all contacts,
and access specific contact details using their primary key (pk).

URL Patterns:
- `''`: POST to create a new contact request or GET to list all contacts.
- `'<int:pk>/'`: GET to retrieve a specific contact, DELETE to remove it,
and potentially 
  other HTTP methods for updating (depending on the view implementation).
"""


from django.urls import path
from .views import ContactView

urlpatterns = [
    path('', ContactView.as_view(), name='contact'),
    path('<int:pk>/', ContactView.as_view(), name='contact-detail'),
]
