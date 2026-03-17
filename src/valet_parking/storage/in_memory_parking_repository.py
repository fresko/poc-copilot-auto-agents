"""In-memory implementation of parking facility repository."""

import threading
from uuid import UUID

from valet_parking.models.parking import Parking


class InMemoryParkingRepository:
    """Thread-safe in-memory storage for parking facilities.

    Uses a dictionary to store parking facilities by UUID. Thread-safe operations
    are ensured using a threading lock.
    """

    def __init__(self) -> None:
        """Initialize empty in-memory repository."""
        self._parkings: dict[UUID, Parking] = {}
        self._lock = threading.Lock()

    def save(self, parking: Parking) -> None:
        """Save a new parking facility to memory.

        Args:
            parking: Parking facility to save.
        """
        with self._lock:
            self._parkings[parking.parking_id] = parking

    def find_by_id(self, parking_id: UUID) -> Parking | None:
        """Find a parking facility by its ID.

        Args:
            parking_id: Unique parking facility identifier.

        Returns:
            Parking facility if found, None otherwise.
        """
        with self._lock:
            return self._parkings.get(parking_id)

    def find_all(self) -> list[Parking]:
        """Find all parking facilities.

        Returns:
            List of all parking facilities.
        """
        with self._lock:
            return list(self._parkings.values())

    def update(self, parking: Parking) -> None:
        """Update an existing parking facility in memory.

        Args:
            parking: Parking facility with updated data.
        """
        with self._lock:
            self._parkings[parking.parking_id] = parking

    def delete(self, parking_id: UUID) -> None:
        """Delete a parking facility from memory.

        Args:
            parking_id: ID of parking facility to delete.
        """
        with self._lock:
            self._parkings.pop(parking_id, None)
