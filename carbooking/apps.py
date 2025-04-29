from django.apps import AppConfig


class CarbookingConfig(AppConfig):
    """
    Django application configuration for the Car Booking app.

    This class is responsible for configuring the Car Booking application
    within the Django project, specifying settings such as the default
    auto field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carbooking'
