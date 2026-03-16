"""Validation utilities for customer and vehicle data."""

import re

from valet_parking.exceptions import InvalidPhoneNumberError, InvalidVehiclePlateError


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format.

    Supports international formats including:
    - +1-555-0123
    - (555) 123-4567
    - 555.123.4567
    - 5551234567

    Args:
        phone: Phone number string to validate.

    Returns:
        True if valid.

    Raises:
        InvalidPhoneNumberError: If phone number is invalid.
    """
    if not phone or not phone.strip():
        raise InvalidPhoneNumberError("Phone number cannot be empty")

    # Remove common separators
    cleaned = re.sub(r"[\s\-\.\(\)]", "", phone)

    # Check for valid international format or US format
    # International: starts with +, followed by 7-15 digits
    # US: 10 digits
    if cleaned.startswith("+"):
        if not re.match(r"^\+\d{7,15}$", cleaned):
            raise InvalidPhoneNumberError(f"Invalid international phone number format: {phone}")
    else:
        if not re.match(r"^\d{10}$", cleaned):
            raise InvalidPhoneNumberError(
                f"Invalid phone number format (expected 10 digits): {phone}"
            )

    return True


def validate_license_plate(plate: str) -> bool:
    """Validate license plate format.

    Basic alphanumeric validation supporting various formats.

    Args:
        plate: License plate string to validate.

    Returns:
        True if valid.

    Raises:
        InvalidVehiclePlateError: If license plate is invalid.
    """
    if not plate or not plate.strip():
        raise InvalidVehiclePlateError("License plate cannot be empty")

    cleaned = plate.strip().upper()

    # Basic validation: 2-10 alphanumeric characters, may include spaces/hyphens
    if not re.match(r"^[A-Z0-9\s\-]{2,10}$", cleaned):
        raise InvalidVehiclePlateError(
            f"Invalid license plate format (expected 2-10 alphanumeric characters): {plate}"
        )

    # Must contain at least one alphanumeric character
    if not re.search(r"[A-Z0-9]", cleaned):
        raise InvalidVehiclePlateError(
            f"License plate must contain alphanumeric characters: {plate}"
        )

    return True


def sanitize_plate_number(plate: str) -> str:
    """Sanitize license plate by removing special characters and converting to uppercase.

    Args:
        plate: License plate string to sanitize.

    Returns:
        Sanitized license plate string.
    """
    # Remove special characters except spaces and hyphens
    sanitized = re.sub(r"[^A-Z0-9\s\-]", "", plate.upper())
    return sanitized.strip()
