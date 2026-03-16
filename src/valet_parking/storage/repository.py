"""Repository interface for reservation data persistence."""

from typing import Protocol
from uuid import UUID

from valet_parking.models.reservation import Reservation


class ReservationRepository(Protocol):
    """Protocol defining the interface for reservation data persistence.

    Implementations must provide methods for CRUD operations on reservations.
    """

    def save(self, reservation: Reservation) -> None:
        """Save a new reservation.

        Args:
            reservation: Reservation to save.
        """
        ...

    def find_by_id(self, reservation_id: UUID) -> Reservation | None:
        """Find a reservation by its ID.

        Args:
            reservation_id: Unique reservation identifier.

        Returns:
            Reservation if found, None otherwise.
        """
        ...

    def find_active_reservations(self) -> list[Reservation]:
        """Find all active reservations.

        Returns:
            List of active reservations.
        """
        ...

    def update(self, reservation: Reservation) -> None:
        """Update an existing reservation.

        Args:
            reservation: Reservation with updated data.
        """
        ...

    def delete(self, reservation_id: UUID) -> None:
        """Delete a reservation.

        Args:
            reservation_id: ID of reservation to delete.
        """
        ...
