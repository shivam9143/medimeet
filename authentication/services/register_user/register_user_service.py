import injector
from rest_framework import status

from authentication.serializers import UserSerializer
from authentication.services.otp.send_otp_service import SendOTPService
from core.create_response import create_response


class UserRegistrationService:
    @injector.inject
    def __init__(self, send_otp_service: SendOTPService):
        self.otp_sending_service = send_otp_service

    def register_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']

            response = self.otp_sending_service.handle_otp_sending(mobile_number)

            if response.data['code'] == status.HTTP_201_CREATED:
                serializer.save(is_verified=False)
            return response

        # Serialize the error details to extract actual messages (strings)
        error_details = {key: [str(value[0])] for key, value in serializer.errors.items()}


        return create_response(code=status.HTTP_400_BAD_REQUEST, error=error_details,
                               message="Something went wrong!")
