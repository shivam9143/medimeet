from django.contrib.auth import get_user_model
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.models import User


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Override this method to fetch user using UUID instead of integer ID.
        """
        user_id = validated_token.get('user_id')  # Assuming user_id is in the token
        # print(f"user id {user_id}")
        # User = get_user_model()

        # Adjust to handle UUID
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
