class OTPServiceInterface:

    # URL construction logic here
    def construct_send_otp_url(self, mobile_number):
        pass

    def construct_verify_otp_url(self, mobile_number, verification_id, otp_code):
        pass

    # def generate_otp(self):
    #     pass

    # def is_retry_allowed(self, mobile_number):
    #     pass
    #
    # def store_otp(self, mobile_number, otp):
    #     pass
    #
    # def read_otp(self, mobile_number, otp):
    #     pass

    def send_otp(self, mobile_number, otp):
        pass
