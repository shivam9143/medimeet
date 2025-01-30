from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from core.logging_config import medimeetlogger


def validate_mobile_number(mobile_number):
    """
    Validates the mobile number format.
    """
    validator = RegexValidator(
        regex=r"^\d{10}$",
        message="Invalid mobile number format. Must be 10 digits."
    )
    try:
        validator(mobile_number)
    except ValidationError as e:
        medimeetlogger.error(f"Invalid mobile number: {mobile_number}")
        raise ValueError(f"Invalid mobile number: {str(e)}")
