from rest_framework.response import Response

from core.base_response_serializer import BaseResponseSerializer


def create_response(code: int, message: str, error: str = None, data: dict = None):
    response_data = {
        "code": code,
        "message": message,
        "error": error,
        "data": data or None,
    }
    return Response(BaseResponseSerializer(response_data).data, status=code)