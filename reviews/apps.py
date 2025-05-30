from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Configuration for the 'reviews' app.

    Sets the default auto field type and the app name used by Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
