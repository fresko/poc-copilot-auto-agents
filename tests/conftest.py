"""Shared test fixtures for valet parking tests."""

import pytest
from uuid import uuid4
from datetime import datetime

from valet_parking.core.qr_generator import QRCodeGenerator
from valet_parking.core.reservation_service import ReservationService
from valet_parking.core.time_calculator import TimeCalculator
from valet_parking.models.reservation import Customer, Reservation, ReservationStatus, Vehicle
from valet_parking.storage.in_memory_repository import InMemoryReservationRepository


@pytest.fixture
def repository():
    """Provide an in-memory repository instance."""
    return InMemoryReservationRepository()


@pytest.fixture
def qr_generator():
    """Provide a QR code generator instance."""
    return QRCodeGenerator()


@pytest.fixture
def time_calculator():
    """Provide a time calculator instance."""
    return TimeCalculator()


@pytest.fixture
def reservation_service(repository, qr_generator, time_calculator):
    """Provide a configured reservation service."""
    return ReservationService(repository, qr_generator, time_calculator)


@pytest.fixture
def sample_customer_data():
    """Provide valid customer data for testing."""
    return {
        "mobile_number": "+1-555-0123",
        "full_name": "John Doe",
    }


@pytest.fixture
def sample_vehicle_data():
    """Provide valid vehicle data for testing."""
    return {
        "license_plate": "ABC123",
        "key_scan_data": "KEY_SCAN_DATA",
        "damage_report": "Small scratch on rear bumper",
    }


@pytest.fixture
def sample_reservation(qr_generator):
    """Provide a pre-created reservation for testing."""
    customer = Customer(mobile_number="+1-555-0123", full_name="John Doe")
    vehicle = Vehicle(
        license_plate="ABC123",
        key_scan_data="KEY_SCAN_DATA",
        damage_report="Small scratch on rear bumper",
    )

    reservation_id = uuid4()
    qr_code_data = qr_generator.generate_qr_data(reservation_id)

    return Reservation(
        reservation_id=reservation_id,
        customer=customer,
        vehicle=vehicle,
        check_in_time=datetime.now(),
        qr_code_data=qr_code_data,
        status=ReservationStatus.ACTIVE,
    )
