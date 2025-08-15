# accounts/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email
    instead of the default username.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate a user based on email and password.

        Args:
            request: The current HTTP request object (can be None in some cases).
            email (str): The email entered by the user.
            password (str): The password entered by the user.
            **kwargs: Additional keyword arguments (ignored here).

        Returns:
            User object if authentication is successful, otherwise None.
        """
        UserModel = get_user_model()

        try:
            # Attempt to retrieve the user by email
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # Return None if no user matches the given email
            return None
        else:
            # Verify the provided password and ensure the account is active
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        # Return None if authentication fails
        return None
