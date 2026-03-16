"""Tests for reservation service."""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from valet_parking.exceptions import (
    InvalidPhoneNumberError,
    InvalidVehiclePlateError,
    ReservationAlreadyClosedError,
    ReservationNotFoundError,
)
from valet_parking.models.reservation import ReservationStatus


class TestReservationService:
    """Tests for ReservationService class."""

    def test_create_reservation_valid_data_creates_and_saves(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that creating a reservation with valid data succeeds."""
        reservation = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
            key_scan_data=sample_vehicle_data["key_scan_data"],
            damage_report=sample_vehicle_data["damage_report"],
        )

        assert reservation is not None
        assert reservation.customer.mobile_number == sample_customer_data["mobile_number"]
        assert reservation.customer.full_name == sample_customer_data["full_name"]
        assert reservation.vehicle.license_plate == sample_vehicle_data["license_plate"]
        assert reservation.status == ReservationStatus.ACTIVE

    def test_create_reservation_generates_qr_code(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that creating a reservation generates a QR code."""
        reservation = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
        )

        assert reservation.qr_code_data is not None
        assert len(reservation.qr_code_data) > 0

    def test_create_reservation_invalid_phone_raises_error(
        self, reservation_service, sample_vehicle_data
    ):
        """Test that invalid phone number raises error."""
        with pytest.raises(InvalidPhoneNumberError):
            reservation_service.create_reservation(
                mobile_number="123",
                full_name="John Doe",
                license_plate=sample_vehicle_data["license_plate"],
            )

    def test_create_reservation_invalid_plate_raises_error(
        self, reservation_service, sample_customer_data
    ):
        """Test that invalid license plate raises error."""
        with pytest.raises(InvalidVehiclePlateError):
            reservation_service.create_reservation(
                mobile_number=sample_customer_data["mobile_number"],
                full_name=sample_customer_data["full_name"],
                license_plate="",
            )

    def test_get_reservation_existing_returns_reservation(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that getting an existing reservation returns it."""
        created = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
        )

        retrieved = reservation_service.get_reservation(created.reservation_id)

        assert retrieved is not None
        assert retrieved.reservation_id == created.reservation_id

    def test_get_reservation_nonexistent_raises_error(self, reservation_service):
        """Test that getting a non-existent reservation raises error."""
        non_existent_id = uuid4()

        with pytest.raises(ReservationNotFoundError):
            reservation_service.get_reservation(non_existent_id)

    def test_close_reservation_sets_checkout_time(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that closing a reservation sets the checkout time."""
        created = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
        )

        closed = reservation_service.close_reservation(created.reservation_id)

        assert closed.check_out_time is not None
        assert closed.check_out_time > created.check_in_time

    def test_close_reservation_updates_status_to_completed(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that closing a reservation updates status to COMPLETED."""
        created = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
        )

        closed = reservation_service.close_reservation(created.reservation_id)

        assert closed.status == ReservationStatus.COMPLETED

    def test_close_reservation_already_closed_raises_error(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that closing an already closed reservation raises error."""
        created = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
        )

        # Close once
        reservation_service.close_reservation(created.reservation_id)

        # Try to close again
        with pytest.raises(ReservationAlreadyClosedError):
            reservation_service.close_reservation(created.reservation_id)

    def test_calculate_current_duration_returns_time_elapsed(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that calculating current duration returns time elapsed."""
        created = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
        )

        duration = reservation_service.calculate_current_duration(created.reservation_id)

        # Duration should be very small (just created)
        assert duration >= timedelta(0)
        assert duration < timedelta(seconds=5)

    def test_update_vehicle_damage_modifies_damage_report(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that updating vehicle damage modifies the damage report."""
        created = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
            damage_report="Original damage",
        )

        updated = reservation_service.update_vehicle_damage(
            created.reservation_id, "New damage report"
        )

        assert updated.vehicle.damage_report == "New damage report"

    def test_get_active_reservations_returns_active_only(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test that get_active_reservations returns only active reservations."""
        # Create 2 active reservations
        reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name="Customer 1",
            license_plate="ABC123",
        )

        reservation2 = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name="Customer 2",
            license_plate="XYZ789",
        )

        # Close one reservation
        reservation_service.close_reservation(reservation2.reservation_id)

        # Get active reservations
        active = reservation_service.get_active_reservations()

        assert len(active) == 1
        assert active[0].customer.full_name == "Customer 1"
