"""In-memory implementation of reservation repository."""

import threading
from uuid import UUID

from valet_parking.models.reservation import Reservation, ReservationStatus


class InMemoryReservationRepository:
    """Thread-safe in-memory storage for reservations.

    Uses a dictionary to store reservations by UUID. Thread-safe operations
    are ensured using a threading lock.
    """

    def __init__(self) -> None:
        """Initialize empty in-memory repository."""
        self._reservations: dict[UUID, Reservation] = {}
        self._lock = threading.Lock()

    def save(self, reservation: Reservation) -> None:
        """Save a new reservation to memory.

        Args:
            reservation: Reservation to save.
        """
        with self._lock:
            self._reservations[reservation.reservation_id] = reservation

    def find_by_id(self, reservation_id: UUID) -> Reservation | None:
        """Find a reservation by its ID.

        Args:
            reservation_id: Unique reservation identifier.

        Returns:
            Reservation if found, None otherwise.
        """
        with self._lock:
            return self._reservations.get(reservation_id)

    def find_active_reservations(self) -> list[Reservation]:
        """Find all active reservations.

        Returns:
            List of reservations with ACTIVE status.
        """
        with self._lock:
            return [
                reservation
                for reservation in self._reservations.values()
                if reservation.status == ReservationStatus.ACTIVE
            ]

    def update(self, reservation: Reservation) -> None:
        """Update an existing reservation in memory.

        Args:
            reservation: Reservation with updated data.
        """
        with self._lock:
            self._reservations[reservation.reservation_id] = reservation

    def delete(self, reservation_id: UUID) -> None:
        """Delete a reservation from memory.

        Args:
            reservation_id: ID of reservation to delete.
        """
        with self._lock:
            self._reservations.pop(reservation_id, None)
