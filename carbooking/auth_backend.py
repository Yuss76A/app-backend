from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Authentication backend that authenticates users by their email address.

    This custom backend allows users to log in using their email instead of a
    username.
    It retrieves the user model defined in the settings' AUTH_USER_MODEL and
    checks the provided credentials against the email and password.

    Methods:
        authenticate(request, username=None, password=None, **kwargs):
            Authenticates a user based on the provided email and password.
            Returns a User instance if authentication is successful, or None
            if it fails.

    Attributes:
        UserModel (Model): The user model that is retrieved using
        get_user_model().
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Attempt to get the user by email (username in this context)
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            # Check if the password is correct
            if user.check_password(password):
                return user
        return None
