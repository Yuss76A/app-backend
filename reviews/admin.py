"""
This module registers the Review model with Django's admin site,
allowing administrators to manage reviews through the admin interface.
"""


from django.contrib import admin
from .models import Review

admin.site.register(Review)
