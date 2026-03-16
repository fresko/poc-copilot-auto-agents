"""Data models for valet parking reservations."""

from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class ReservationStatus(str, Enum):
    """Status of a parking reservation."""

    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Customer(BaseModel):
    """Customer information for a valet parking reservation.

    Attributes:
        mobile_number: Customer's mobile phone number.
        full_name: Customer's full name (minimum 2 characters).
    """

    mobile_number: str
    full_name: str = Field(min_length=2)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        """Validate that full name has at least 2 characters."""
        if len(v.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters")
        return v.strip()


class Vehicle(BaseModel):
    """Vehicle information for a valet parking reservation.

    Attributes:
        license_plate: Vehicle's license plate number.
        damage_report: Optional description of pre-existing damage.
        key_scan_data: Optional scanned key or plate data.
    """

    license_plate: str
    damage_report: str | None = None
    key_scan_data: str | None = None

    @field_validator("license_plate")
    @classmethod
    def validate_license_plate(cls, v: str) -> str:
        """Validate and sanitize license plate."""
        if not v or not v.strip():
            raise ValueError("License plate cannot be empty")
        return v.strip().upper()


class Reservation(BaseModel):
    """A valet parking reservation.

    Attributes:
        reservation_id: Unique identifier for the reservation.
        customer: Customer information.
        vehicle: Vehicle information.
        check_in_time: Time when vehicle was checked in.
        check_out_time: Time when vehicle was checked out (None if still parked).
        qr_code_data: QR code data for quick retrieval.
        status: Current status of the reservation.
        parking_duration: Calculated parking duration (None until checkout).
    """

    reservation_id: UUID = Field(default_factory=uuid4)
    customer: Customer
    vehicle: Vehicle
    check_in_time: datetime = Field(default_factory=datetime.now)
    check_out_time: datetime | None = None
    qr_code_data: str
    status: ReservationStatus = ReservationStatus.ACTIVE
    parking_duration: timedelta | None = None

    @property
    def current_duration(self) -> timedelta:
        """Calculate current parking duration.

        Returns:
            Time elapsed since check-in to checkout (or now if not checked out).
        """
        end_time = self.check_out_time if self.check_out_time else datetime.now()
        return end_time - self.check_in_time

    def is_active(self) -> bool:
        """Check if reservation is currently active.

        Returns:
            True if status is ACTIVE, False otherwise.
        """
        return self.status == ReservationStatus.ACTIVE

    def is_completed(self) -> bool:
        """Check if reservation is completed.

        Returns:
            True if status is COMPLETED, False otherwise.
        """
        return self.status == ReservationStatus.COMPLETED
