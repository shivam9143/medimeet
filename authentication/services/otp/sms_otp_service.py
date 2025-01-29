import random

import injector

from authentication.services.otp.otp_service_interface import OTPServiceInterface
from core.logging_config import medimeetlogger
# from core.redis_service import RedisService
from core.request_client import RequestSingleton
from medimeet.settings import env


class SMSOTPServiceInterface(OTPServiceInterface):
    """
     Handles sending OTPs via an external API.
     """

    @injector.inject
    def __init__(self):
        self.base_url = env('CPaaS_BASE_URL')
        self.verify_otp = env('VERIFY_OTP_ENDPOINT')
        self.endpoint = env('OTP_ENDPOINT')
        self.customer_id = env('CUSTOMER_ID')
        self.flow_type = env('FLOW_TYPE')
        self.auth_token = env('SMS_API_AUTH_TOKEN')
        self.country_code = env('COUNTRY_CODE', default='91')  # Default to India
        self.otp_length = env('OTP_LENGTH', default='6')  # Default to 6 digits
        # self.redis_service = rs

    def construct_send_otp_url(self, mobile_number):
        """
        Constructs the API URL for sending the OTP.
        """
        return (
            f"{self.base_url}{self.endpoint}"
            f"?countryCode={self.country_code}"
            f"&otpLength={self.otp_length}"
            f"&customerId={self.customer_id}"
            f"&flowType={self.flow_type}"
            f"&mobileNumber={mobile_number}"
        )

    def construct_verify_otp_url(self, mobile_number, verification_id, otp_code):
        """
        Constructs the API URL for verifying the OTP.
        """
        return (
            f"{self.base_url}{self.verify_otp}"
            f"?countryCode={self.country_code}"
            f"&mobileNumber={mobile_number}"
            f"&verificationId={verification_id}"
            f"&customerId={self.customer_id}"
            f"&code={otp_code}"
        )

    # def generate_otp(self):
    #     return f"{random.randint(100000, 999999)}"

    # def is_retry_allowed(self, mobile_number):
    #     return self.redis_service.is_retry_allowed(mobile_number=mobile_number)
    #
    # def store_otp(self, mobile_number, otp):
    #     self.redis_service.store_otp(mobile_number=mobile_number, otp=otp)

    def send_otp(self, mobile_number, otp):
        """
        Sends the OTP to the given mobile number via SMS.

        Args:
            mobile_number (str): The recipient's mobile number.
            otp (str): The OTP to send.

        Returns:
            dict: Response from the external API.
        """

        """
        Sends the OTP via the external API.
        """
        url = self.construct_send_otp_url(mobile_number)
        headers = {"authToken": self.auth_token}

        try:
            response = RequestSingleton.post(url, headers=headers)
            # response.raise_for_status()
            medimeetlogger.debug(f"OTP sent successfully. Response: {response.text}")
            return response.json()
        except RequestSingleton.get_exceptions().RequestException as e:
            medimeetlogger.error(f"Failed to send OTP: {str(e)}")
            raise

    def validate_otp_api(self, mobile_number, verification_id, otp_code):
        """
            Validates the OTP using the provided API.
            :param mobile_number: str - The mobile number where the OTP was sent.
            :param verification_id: str - The verification ID associated with the OTP.
            :param otp_code: str - The OTP code to validate.
            :param auth_token: str - The authorization token for the API.
            :return: dict - The response from the API.
            """

        url = self.construct_verify_otp_url(mobile_number, verification_id=verification_id, otp_code=otp_code)
        headers = {"authToken": self.auth_token}

        try:
            response = RequestSingleton.get(url, headers=headers)
            medimeetlogger.debug(response.text)
            # response.raise_for_status()
            response_data = response.json()
            response_code = response_data.get("responseCode")
            if response_code == 200:
                return True, "OTP validated successfully."
            elif response_code == 400:
                return False, "Bad request. Please check the input parameters."
            elif response_code == 409:
                return False, "Duplicate resource. The request already exists."
            elif response_code == 500:
                return False, "Server error. Please try again later."
            elif response_code == 501:
                return False, "Invalid customer ID."
            elif response_code == 505:
                return False, "Invalid verification ID."
            elif response_code == 506:
                return False, "Request already exists."
            elif response_code == 511:
                return False, "Invalid country code."
            elif response_code == 700:
                return False, "Verification failed. Please try again."
            elif response_code == 702:
                return False, "Wrong OTP provided. Please check and try again."
            elif response_code == 703:
                return False, "Already verified."
            elif response_code == 705:
                return False, "Verification expired. Please request a new OTP."
            elif response_code == 800:
                return False, "Maximum limit reached. Please try again later."
            else:
                return False, f"Unexpected response code: {response_code}"
        except RequestSingleton.get_exceptions().RequestException as e:
            medimeetlogger.error(f"Failed to verify OTP: {str(e)}")
            raise
