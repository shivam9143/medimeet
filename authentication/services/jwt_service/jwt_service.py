import jwt

from medimeet import settings


class JWTService:
    def generate_jwt(self, user):
        payload = {
            "id": user["id"],
            "mobile_number": user["mobile_number"],
            "exp": settings.JWT_EXPIRATION_TIME,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")