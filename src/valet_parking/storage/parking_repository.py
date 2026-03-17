"""Repository interface for parking facility data persistence."""

from typing import Protocol
from uuid import UUID

from valet_parking.models.parking import Parking


class ParkingRepository(Protocol):
    """Protocol defining the interface for parking facility data persistence.

    Implementations must provide methods for CRUD operations on parking facilities.
    """

    def save(self, parking: Parking) -> None:
        """Save a new parking facility.

        Args:
            parking: Parking facility to save.
        """
        ...

    def find_by_id(self, parking_id: UUID) -> Parking | None:
        """Find a parking facility by its ID.

        Args:
            parking_id: Unique parking facility identifier.

        Returns:
            Parking facility if found, None otherwise.
        """
        ...

    def find_all(self) -> list[Parking]:
        """Find all parking facilities.

        Returns:
            List of all parking facilities.
        """
        ...

    def update(self, parking: Parking) -> None:
        """Update an existing parking facility.

        Args:
            parking: Parking facility with updated data.
        """
        ...

    def delete(self, parking_id: UUID) -> None:
        """Delete a parking facility.

        Args:
            parking_id: ID of parking facility to delete.
        """
        ...
