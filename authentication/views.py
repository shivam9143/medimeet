import injector
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.create_response import create_response
from .di.injector_config import auth_injector_instance
from .serializers import OTPVerificationSerializer
from authentication.services.verify_otp.otp_verification_service import OTPVerificationService
from authentication.services.register_user.register_user_service import UserRegistrationService, SendOTPService


class RegisterUserAPIView(APIView):
    @injector.inject
    def __init__(self, **kwargs):
        self.user_registration_service = auth_injector_instance.get(UserRegistrationService)

    def post(self, request):
        # Delegate the registration logic to the UserRegistrationService
        response = self.user_registration_service.register_user(request)

        # Return the response returned from the service
        return response


class SendOtpAPIView(APIView):
    @injector.inject
    def __init__(self, **kwargs):
        self.send_otp_service = auth_injector_instance.get(SendOTPService)

    def post(self, request):
        # Delegate the send otp logic to the UserRegistrationService
        response = self.send_otp_service.send_otp(request)

        # Return the response returned from the service
        return response


class VerifyOTPAPIView(APIView):
    """
    View for verifying User.
    """

    @injector.inject
    def __init__(self, **kwargs):
        self.otp_verification_service = auth_injector_instance.get(OTPVerificationService)

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)

        if serializer.is_valid():
            mobile_number = serializer.validated_data["mobile_number"]
            otp = serializer.validated_data["otp"]
            verification_id = serializer.validated_data["verification_id"]

            # Delegate the verification to the service
            return self.otp_verification_service.verify_user(mobile_number, otp, verification_id)

        # Serialize the error details to extract actual messages (strings)
        # error_details = {key: [str(value[0])] for key, value in serializer.errors.items()}

        return create_response(error="error_details", code=status.HTTP_400_BAD_REQUEST, message="Something went wrong")
