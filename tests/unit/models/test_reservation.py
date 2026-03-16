"""Tests for reservation data models."""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from valet_parking.models.reservation import (
    Customer,
    Reservation,
    ReservationStatus,
    Vehicle,
)


class TestCustomer:
    """Tests for Customer model."""

    def test_customer_creation_valid_data_creates_customer(self):
        """Test that valid data creates a customer successfully."""
        customer = Customer(mobile_number="+1-555-0123", full_name="John Doe")

        assert customer.mobile_number == "+1-555-0123"
        assert customer.full_name == "John Doe"

    def test_customer_creation_invalid_phone_raises_error(self):
        """Test that customer creation with short name raises validation error."""
        with pytest.raises(ValueError, match="at least 2 characters"):
            Customer(mobile_number="+1-555-0123", full_name="J")

    def test_customer_full_name_strips_whitespace(self):
        """Test that full name is stripped of whitespace."""
        customer = Customer(mobile_number="+1-555-0123", full_name="  John Doe  ")
        assert customer.full_name == "John Doe"


class TestVehicle:
    """Tests for Vehicle model."""

    def test_vehicle_creation_valid_data_creates_vehicle(self):
        """Test that valid data creates a vehicle successfully."""
        vehicle = Vehicle(
            license_plate="ABC123",
            damage_report="Scratch on bumper",
            key_scan_data="KEY123",
        )

        assert vehicle.license_plate == "ABC123"
        assert vehicle.damage_report == "Scratch on bumper"
        assert vehicle.key_scan_data == "KEY123"

    def test_vehicle_creation_invalid_plate_raises_error(self):
        """Test that empty license plate raises validation error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Vehicle(license_plate="")

    def test_vehicle_license_plate_uppercase_conversion(self):
        """Test that license plate is converted to uppercase."""
        vehicle = Vehicle(license_plate="abc123")
        assert vehicle.license_plate == "ABC123"

    def test_vehicle_optional_fields_default_to_none(self):
        """Test that optional fields default to None."""
        vehicle = Vehicle(license_plate="ABC123")
        assert vehicle.damage_report is None
        assert vehicle.key_scan_data is None


class TestReservation:
    """Tests for Reservation model."""

    def test_reservation_creation_valid_data_creates_reservation(
        self, sample_customer_data, sample_vehicle_data, qr_generator
    ):
        """Test that valid data creates a reservation successfully."""
        customer = Customer(**sample_customer_data)
        vehicle = Vehicle(**sample_vehicle_data)
        reservation_id = uuid4()
        qr_code_data = qr_generator.generate_qr_data(reservation_id)

        reservation = Reservation(
            reservation_id=reservation_id,
            customer=customer,
            vehicle=vehicle,
            qr_code_data=qr_code_data,
        )

        assert reservation.reservation_id == reservation_id
        assert reservation.customer == customer
        assert reservation.vehicle == vehicle
        assert reservation.qr_code_data == qr_code_data

    def test_reservation_has_unique_id(self):
        """Test that each reservation gets a unique ID."""
        customer = Customer(mobile_number="+1-555-0123", full_name="John Doe")
        vehicle = Vehicle(license_plate="ABC123")

        reservation1 = Reservation(customer=customer, vehicle=vehicle, qr_code_data="QR1")
        reservation2 = Reservation(customer=customer, vehicle=vehicle, qr_code_data="QR2")

        assert reservation1.reservation_id != reservation2.reservation_id

    def test_reservation_status_defaults_to_active(self):
        """Test that reservation status defaults to ACTIVE."""
        customer = Customer(mobile_number="+1-555-0123", full_name="John Doe")
        vehicle = Vehicle(license_plate="ABC123")

        reservation = Reservation(customer=customer, vehicle=vehicle, qr_code_data="QR123")

        assert reservation.status == ReservationStatus.ACTIVE

    def test_reservation_parking_duration_calculated_correctly(self):
        """Test that parking duration property calculates correctly."""
        customer = Customer(mobile_number="+1-555-0123", full_name="John Doe")
        vehicle = Vehicle(license_plate="ABC123")

        check_in = datetime(2024, 1, 15, 10, 0)
        check_out = datetime(2024, 1, 15, 12, 30)

        reservation = Reservation(
            customer=customer,
            vehicle=vehicle,
            qr_code_data="QR123",
            check_in_time=check_in,
            check_out_time=check_out,
        )

        expected_duration = timedelta(hours=2, minutes=30)
        # Using the current_duration property
        assert abs(reservation.current_duration - expected_duration) < timedelta(seconds=1)

    def test_reservation_is_active_returns_true_for_active(self):
        """Test is_active() returns True for active reservations."""
        customer = Customer(mobile_number="+1-555-0123", full_name="John Doe")
        vehicle = Vehicle(license_plate="ABC123")

        reservation = Reservation(
            customer=customer,
            vehicle=vehicle,
            qr_code_data="QR123",
            status=ReservationStatus.ACTIVE,
        )

        assert reservation.is_active() is True

    def test_reservation_is_completed_returns_true_for_completed(self):
        """Test is_completed() returns True for completed reservations."""
        customer = Customer(mobile_number="+1-555-0123", full_name="John Doe")
        vehicle = Vehicle(license_plate="ABC123")

        reservation = Reservation(
            customer=customer,
            vehicle=vehicle,
            qr_code_data="QR123",
            status=ReservationStatus.COMPLETED,
        )

        assert reservation.is_completed() is True
