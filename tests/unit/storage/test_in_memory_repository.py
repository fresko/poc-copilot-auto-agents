"""Tests for in-memory repository."""

import threading
from uuid import uuid4

import pytest

from valet_parking.models.reservation import ReservationStatus


class TestInMemoryRepository:
    """Tests for InMemoryReservationRepository class."""

    def test_save_reservation_stores_correctly(self, repository, sample_reservation):
        """Test that saving a reservation stores it correctly."""
        repository.save(sample_reservation)

        found = repository.find_by_id(sample_reservation.reservation_id)
        assert found is not None
        assert found.reservation_id == sample_reservation.reservation_id

    def test_find_by_id_existing_reservation_returns_reservation(
        self, repository, sample_reservation
    ):
        """Test that finding an existing reservation returns it."""
        repository.save(sample_reservation)

        found = repository.find_by_id(sample_reservation.reservation_id)

        assert found is not None
        assert found.reservation_id == sample_reservation.reservation_id
        assert found.customer.full_name == sample_reservation.customer.full_name

    def test_find_by_id_nonexistent_returns_none(self, repository):
        """Test that finding a non-existent reservation returns None."""
        non_existent_id = uuid4()

        found = repository.find_by_id(non_existent_id)

        assert found is None

    def test_update_reservation_modifies_existing(self, repository, sample_reservation):
        """Test that updating a reservation modifies the existing one."""
        repository.save(sample_reservation)

        # Modify the reservation
        sample_reservation.vehicle.damage_report = "New damage report"
        repository.update(sample_reservation)

        # Retrieve and verify
        found = repository.find_by_id(sample_reservation.reservation_id)
        assert found.vehicle.damage_report == "New damage report"

    def test_delete_reservation_removes_from_storage(self, repository, sample_reservation):
        """Test that deleting a reservation removes it from storage."""
        repository.save(sample_reservation)

        # Delete the reservation
        repository.delete(sample_reservation.reservation_id)

        # Should not be found
        found = repository.find_by_id(sample_reservation.reservation_id)
        assert found is None

    def test_find_active_reservations_returns_only_active(self, repository, qr_generator):
        """Test that find_active_reservations returns only active reservations."""
        from valet_parking.models.reservation import Customer, Reservation, Vehicle

        # Create multiple reservations with different statuses
        for i in range(3):
            customer = Customer(mobile_number=f"+1-555-{i:04d}", full_name=f"Customer {i}")
            vehicle = Vehicle(license_plate=f"ABC{i:03d}")
            reservation_id = uuid4()
            qr_code_data = qr_generator.generate_qr_data(reservation_id)

            status = ReservationStatus.ACTIVE if i < 2 else ReservationStatus.COMPLETED

            reservation = Reservation(
                reservation_id=reservation_id,
                customer=customer,
                vehicle=vehicle,
                qr_code_data=qr_code_data,
                status=status,
            )
            repository.save(reservation)

        # Find active reservations
        active = repository.find_active_reservations()

        assert len(active) == 2
        for reservation in active:
            assert reservation.status == ReservationStatus.ACTIVE

    def test_repository_thread_safe_concurrent_writes(self, repository, qr_generator):
        """Test that repository handles concurrent writes safely."""
        from valet_parking.models.reservation import Customer, Reservation, Vehicle

        def create_reservation(index):
            customer = Customer(mobile_number=f"+1-555-{index:04d}", full_name=f"Customer {index}")
            vehicle = Vehicle(license_plate=f"ABC{index:03d}")
            reservation_id = uuid4()
            qr_code_data = qr_generator.generate_qr_data(reservation_id)

            reservation = Reservation(
                reservation_id=reservation_id,
                customer=customer,
                vehicle=vehicle,
                qr_code_data=qr_code_data,
            )
            repository.save(reservation)

        # Create 10 reservations concurrently
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_reservation, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All reservations should be saved
        active = repository.find_active_reservations()
        assert len(active) == 10
