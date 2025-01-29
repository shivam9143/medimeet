from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt import exceptions

from medimeet import settings




class JWTService:
    def generate_jwt(self, user):
        print("jeh3bdfjhrwf wrffr")

        refresh = RefreshToken.for_user(user)
        print("jeh3bdfjhrwf ")
        # Set expiration of access token (typically 1 hour for access token)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(hours=1))  # Set custom expiration time if required
        return str(access_token)  # Return access token as string
    # return str(access_token)  # Return access token as string

    # Optionally, you can add custom claims if you need to:
    # e.g. adding 'id' or 'mobile_number' as custom claims
    # refresh.payload['id'] = user.id  # Add user id to the payload (optional)
    # refresh.payload['mobile_number'] = user.mobile_number  # Add mobile number if needed

    # Set expiration of access token (typically 1 hour for access token)
    # access_token = refresh.access_token
    # access_token.set_exp(lifetime=timedelta(hours=1))  # Set custom expiration time if required

    # expiration_time = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
    #     uid = user["id"]
    #     print(f"user id == ==== {uid}")
    #     payload = {
    #         "id": user["id"],
    #         "mobile_number": user["mobile_number"],
    #         "exp": expiration_time,
    #         "iat": datetime.utcnow()
    #     }
    #     return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
