import injector

from authentication.services.jwt_service.jwt_service import JWTService
from authentication.services.otp.otp_service_interface import OTPServiceInterface
from authentication.services.verify_otp.otp_verification_service import OTPVerificationService
from authentication.services.register_user.register_user_service import UserRegistrationService
from authentication.services.otp.sms_otp_service import SMSOTPServiceInterface
from authentication.services.user_service.user_service import UserService
from core.redis_client import RedisConnection
from core.redis_client_interfaces import IRedisConnection
from core.redis_service import RedisService


class AuthServiceModule(injector.Module):
    def configure(self, binder: injector.Binder):
        binder.bind(OTPServiceInterface, to=OTPServiceInterface)
        binder.bind(UserRegistrationService, to=UserRegistrationService)
        binder.bind(OTPVerificationService, to=OTPVerificationService)
        binder.bind(SMSOTPServiceInterface, to=SMSOTPServiceInterface)
        binder.bind(JWTService, to=JWTService)
        binder.bind(UserService, to=UserService)
        binder.bind(IRedisConnection, to=RedisConnection)
        binder.bind(RedisService, to=RedisService)


# Auth Injector Instance
auth_injector_instance = injector.Injector(AuthServiceModule())
