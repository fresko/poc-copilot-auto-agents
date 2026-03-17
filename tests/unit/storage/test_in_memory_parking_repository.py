"""Tests for in-memory parking repository."""

import threading
from uuid import uuid4

import pytest

from valet_parking.models.parking import Parking
from valet_parking.storage.in_memory_parking_repository import InMemoryParkingRepository


@pytest.fixture
def parking_repository():
    """Provide an in-memory parking repository instance."""
    return InMemoryParkingRepository()


@pytest.fixture
def sample_parking():
    """Provide a pre-created parking facility for testing."""
    return Parking(name="City Center Parking", address="123 Main St", capacity=200, floors=4)


class TestInMemoryParkingRepository:
    """Tests for InMemoryParkingRepository class."""

    def test_save_parking_stores_correctly(self, parking_repository, sample_parking):
        """Test that saving a parking facility stores it correctly."""
        parking_repository.save(sample_parking)

        found = parking_repository.find_by_id(sample_parking.parking_id)
        assert found is not None
        assert found.parking_id == sample_parking.parking_id

    def test_find_by_id_existing_parking_returns_parking(self, parking_repository, sample_parking):
        """Test that finding an existing parking facility returns it."""
        parking_repository.save(sample_parking)

        found = parking_repository.find_by_id(sample_parking.parking_id)

        assert found is not None
        assert found.parking_id == sample_parking.parking_id
        assert found.name == sample_parking.name

    def test_find_by_id_nonexistent_returns_none(self, parking_repository):
        """Test that finding a non-existent parking facility returns None."""
        found = parking_repository.find_by_id(uuid4())

        assert found is None

    def test_find_all_returns_all_parkings(self, parking_repository):
        """Test that find_all returns all saved parking facilities."""
        for i in range(3):
            parking = Parking(name=f"Parking {i}", address=f"{i} Main St", capacity=100, floors=2)
            parking_repository.save(parking)

        all_parkings = parking_repository.find_all()

        assert len(all_parkings) == 3

    def test_update_parking_modifies_existing(self, parking_repository, sample_parking):
        """Test that updating a parking facility modifies the existing one."""
        parking_repository.save(sample_parking)

        updated = sample_parking.model_copy(update={"capacity": 999})
        parking_repository.update(updated)

        found = parking_repository.find_by_id(sample_parking.parking_id)
        assert found.capacity == 999

    def test_delete_parking_removes_from_storage(self, parking_repository, sample_parking):
        """Test that deleting a parking facility removes it from storage."""
        parking_repository.save(sample_parking)

        parking_repository.delete(sample_parking.parking_id)

        found = parking_repository.find_by_id(sample_parking.parking_id)
        assert found is None

    def test_repository_thread_safe_concurrent_writes(self, parking_repository):
        """Test that repository handles concurrent writes safely."""
        def create_parking(index):
            parking = Parking(
                name=f"Parking {index}",
                address=f"{index} Test St",
                capacity=100 + index,
                floors=1 + (index % 5),
            )
            parking_repository.save(parking)

        threads = [threading.Thread(target=create_parking, args=(i,)) for i in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(parking_repository.find_all()) == 10
