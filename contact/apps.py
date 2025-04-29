from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Django application configuration for the Contact app.

    This class configures the Contact application, allowing Django to
    manage the contact-related features and models of the project.

    Attributes:
        default_auto_field (str): The default type of auto-incrementing field
        for new models in this app (BigAutoField).

        name (str): The name of the application, which is used internally
        by Django.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
