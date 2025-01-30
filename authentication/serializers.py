from rest_framework import serializers

from core.base_response_serializer import BaseResponseSerializer
from .models import User
from .utils.validators.mobilenumber_validator import validate_mobile_number


class UserSerializer(serializers.ModelSerializer):

    class Meta:
            model = User
            fields = ['id', 'name', 'age', 'gender', 'mobile_number', 'photo_url', 'is_verified', 'created_at']
            read_only_fields = ['id', 'created_at']

    def validate_mobile_number(self, value):
        """
        Custom validation for mobile_number to ensure correct format.
        """
        validate_mobile_number(value)  # Call your custom validation method
        return value


class OTPVerificationSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    verification_id = serializers.CharField(max_length=15)


class VerifyMobileNumberSerializer(serializers.Serializer):
    """
    Serializer for OTP verification request.
    """
    mobile_number = serializers.CharField(max_length=15)



class OTPVerificationResponseSerializer(BaseResponseSerializer):
    user = UserSerializer()
    token = serializers.CharField()

    def __init__(self, *args, **kwargs):
        # Set the default message and status code
        if 'message' not in kwargs:
            kwargs['message'] = 'User verified successfully'
        kwargs['code'] = 200
        super().__init__(*args, **kwargs)
