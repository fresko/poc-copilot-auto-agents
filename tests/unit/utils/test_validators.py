"""Tests for validation utilities."""

import pytest

from valet_parking.exceptions import InvalidPhoneNumberError, InvalidVehiclePlateError
from valet_parking.utils.validators import (
    sanitize_plate_number,
    validate_license_plate,
    validate_phone_number,
)


class TestPhoneValidation:
    """Tests for phone number validation."""

    def test_validate_phone_number_valid_formats_returns_true(self):
        """Test that various valid phone formats pass validation."""
        valid_numbers = [
            "+1-555-0123",
            "+15550123456",
            "5551234567",
            "(555) 123-4567",
            "555.123.4567",
        ]

        for number in valid_numbers:
            assert validate_phone_number(number) is True

    def test_validate_phone_number_invalid_format_raises_error(self):
        """Test that invalid phone formats raise InvalidPhoneNumberError."""
        invalid_numbers = [
            "",
            "123",
            "abcdefghij",
            "+1",
            "555-123",
        ]

        for number in invalid_numbers:
            with pytest.raises(InvalidPhoneNumberError):
                validate_phone_number(number)

    def test_validate_phone_number_empty_raises_error(self):
        """Test that empty phone number raises error."""
        with pytest.raises(InvalidPhoneNumberError, match="cannot be empty"):
            validate_phone_number("")


class TestLicensePlateValidation:
    """Tests for license plate validation."""

    def test_validate_license_plate_valid_format_returns_true(self):
        """Test that valid license plate formats pass validation."""
        valid_plates = [
            "ABC123",
            "XYZ-789",
            "CA 1234",
            "TX12345",
        ]

        for plate in valid_plates:
            assert validate_license_plate(plate) is True

    def test_validate_license_plate_invalid_format_raises_error(self):
        """Test that invalid license plate formats raise error."""
        invalid_plates = [
            "",
            "A",
            "ABCDEFGHIJK",  # Too long
            "!!!",
        ]

        for plate in invalid_plates:
            with pytest.raises(InvalidVehiclePlateError):
                validate_license_plate(plate)

    def test_validate_license_plate_empty_raises_error(self):
        """Test that empty license plate raises error."""
        with pytest.raises(InvalidVehiclePlateError, match="cannot be empty"):
            validate_license_plate("")


class TestSanitizePlateNumber:
    """Tests for license plate sanitization."""

    def test_sanitize_plate_number_removes_special_chars(self):
        """Test that special characters are removed."""
        result = sanitize_plate_number("ABC@123#")
        assert "@" not in result
        assert "#" not in result
        assert "ABC123" in result

    def test_sanitize_plate_number_converts_to_uppercase(self):
        """Test that plate is converted to uppercase."""
        result = sanitize_plate_number("abc123")
        assert result == "ABC123"

    def test_sanitize_plate_number_preserves_spaces_and_hyphens(self):
        """Test that spaces and hyphens are preserved."""
        result = sanitize_plate_number("ABC-123")
        assert result == "ABC-123"

        result = sanitize_plate_number("CA 1234")
        assert result == "CA 1234"
