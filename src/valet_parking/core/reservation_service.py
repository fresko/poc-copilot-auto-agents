"""Core reservation service managing the complete reservation lifecycle."""

from datetime import datetime, timedelta
from uuid import UUID

from valet_parking.core.qr_generator import QRCodeGenerator
from valet_parking.core.time_calculator import TimeCalculator
from valet_parking.exceptions import (
    ReservationAlreadyClosedError,
    ReservationNotFoundError,
)
from valet_parking.models.reservation import (
    Customer,
    Reservation,
    ReservationStatus,
    Vehicle,
)
from valet_parking.storage.repository import ReservationRepository
from valet_parking.utils.validators import validate_license_plate, validate_phone_number


class ReservationService:
    """Service managing valet parking reservations.

    Handles the complete lifecycle of reservations from creation to closure,
    including QR code generation, time tracking, and data persistence.
    """

    def __init__(
        self,
        repository: ReservationRepository,
        qr_generator: QRCodeGenerator,
        time_calculator: TimeCalculator,
    ) -> None:
        """Initialize reservation service with dependencies.

        Args:
            repository: Repository for data persistence.
            qr_generator: Generator for QR codes.
            time_calculator: Calculator for time and fees.
        """
        self._repository = repository
        self._qr_generator = qr_generator
        self._time_calculator = time_calculator

    def create_reservation(
        self,
        mobile_number: str,
        full_name: str,
        license_plate: str,
        key_scan_data: str | None = None,
        damage_report: str | None = None,
    ) -> Reservation:
        """Create a new parking reservation.

        Args:
            mobile_number: Customer's mobile phone number.
            full_name: Customer's full name.
            license_plate: Vehicle's license plate number.
            key_scan_data: Optional scanned key/plate data.
            damage_report: Optional pre-existing damage description.

        Returns:
            Created reservation with generated QR code.

        Raises:
            InvalidPhoneNumberError: If phone number is invalid.
            InvalidVehiclePlateError: If license plate is invalid.

        Examples:
            >>> service = ReservationService(repository, qr_gen, time_calc)
            >>> reservation = service.create_reservation(
            ...     mobile_number="+1-555-0123",
            ...     full_name="John Doe",
            ...     license_plate="ABC123"
            ... )
            >>> reservation.status
            <ReservationStatus.ACTIVE: 'active'>
        """
        # Validate inputs
        validate_phone_number(mobile_number)
        validate_license_plate(license_plate)

        # Create customer and vehicle models
        customer = Customer(mobile_number=mobile_number, full_name=full_name)

        vehicle = Vehicle(
            license_plate=license_plate,
            key_scan_data=key_scan_data,
            damage_report=damage_report,
        )

        # Generate QR code data
        from uuid import uuid4

        reservation_id = uuid4()
        qr_code_data = self._qr_generator.generate_qr_data(reservation_id)

        # Create reservation
        reservation = Reservation(
            reservation_id=reservation_id,
            customer=customer,
            vehicle=vehicle,
            check_in_time=datetime.now(),
            qr_code_data=qr_code_data,
            status=ReservationStatus.ACTIVE,
        )

        # Save to repository
        self._repository.save(reservation)

        return reservation

    def get_reservation(self, reservation_id: UUID) -> Reservation:
        """Retrieve a reservation by its ID.

        Args:
            reservation_id: Unique reservation identifier.

        Returns:
            The requested reservation.

        Raises:
            ReservationNotFoundError: If reservation doesn't exist.

        Examples:
            >>> reservation = service.get_reservation(reservation_id)
            >>> print(reservation.customer.full_name)
        """
        reservation = self._repository.find_by_id(reservation_id)

        if reservation is None:
            raise ReservationNotFoundError(f"Reservation not found: {reservation_id}")

        return reservation

    def get_active_reservations(self) -> list[Reservation]:
        """Retrieve all active reservations.

        Returns:
            List of all active reservations.

        Examples:
            >>> active = service.get_active_reservations()
            >>> len(active)
            5
        """
        return self._repository.find_active_reservations()

    def calculate_current_duration(self, reservation_id: UUID) -> timedelta:
        """Calculate current parking duration for a reservation.

        Args:
            reservation_id: Unique reservation identifier.

        Returns:
            Time elapsed since check-in.

        Raises:
            ReservationNotFoundError: If reservation doesn't exist.

        Examples:
            >>> duration = service.calculate_current_duration(reservation_id)
            >>> print(f"Parked for {duration.total_seconds() / 3600:.1f} hours")
        """
        reservation = self.get_reservation(reservation_id)

        return self._time_calculator.calculate_duration(
            check_in=reservation.check_in_time, check_out=reservation.check_out_time
        )

    def close_reservation(self, reservation_id: UUID) -> Reservation:
        """Close a reservation and calculate final parking duration.

        Args:
            reservation_id: Unique reservation identifier.

        Returns:
            Updated reservation with checkout time and final duration.

        Raises:
            ReservationNotFoundError: If reservation doesn't exist.
            ReservationAlreadyClosedError: If reservation is already closed.

        Examples:
            >>> closed = service.close_reservation(reservation_id)
            >>> closed.status
            <ReservationStatus.COMPLETED: 'completed'>
        """
        reservation = self.get_reservation(reservation_id)

        # Check if already closed
        if reservation.status == ReservationStatus.COMPLETED:
            raise ReservationAlreadyClosedError(f"Reservation {reservation_id} is already closed")

        # Update reservation
        reservation.check_out_time = datetime.now()
        reservation.parking_duration = self._time_calculator.calculate_duration(
            check_in=reservation.check_in_time, check_out=reservation.check_out_time
        )
        reservation.status = ReservationStatus.COMPLETED

        # Save updated reservation
        self._repository.update(reservation)

        return reservation

    def update_vehicle_damage(self, reservation_id: UUID, damage_report: str) -> Reservation:
        """Update the damage report for a reservation's vehicle.

        Args:
            reservation_id: Unique reservation identifier.
            damage_report: Updated damage description.

        Returns:
            Updated reservation.

        Raises:
            ReservationNotFoundError: If reservation doesn't exist.

        Examples:
            >>> updated = service.update_vehicle_damage(
            ...     reservation_id,
            ...     "New scratch on passenger door"
            ... )
        """
        reservation = self.get_reservation(reservation_id)

        # Update vehicle damage report
        reservation.vehicle.damage_report = damage_report

        # Save updated reservation
        self._repository.update(reservation)

        return reservation
