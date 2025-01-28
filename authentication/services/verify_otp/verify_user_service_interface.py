from abc import ABC, abstractmethod
from rest_framework.response import Response


class VerifyUserServiceInterface(ABC):
    """
    Interface defining the contract for user verification services.
    """

    @abstractmethod
    def verify_user(self, mobile_number: str, otp: str, verification_id: str) -> Response:
        """
        Verifies the OTP for the provided mobile number.

        Args:
            mobile_number (str): The user's mobile number.
            otp (str): The OTP to verify.

        Returns:
            Response: A Response object indicating success or failure.
        """
        pass
