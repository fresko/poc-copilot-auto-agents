"""Integration tests for complete reservation flow."""

import pytest
from time import sleep

from valet_parking.models.reservation import ReservationStatus


class TestReservationFlow:
    """Integration tests for complete reservation lifecycle."""

    def test_complete_reservation_lifecycle(
        self, reservation_service, sample_customer_data, sample_vehicle_data
    ):
        """Test the complete reservation lifecycle from creation to closure.

        This integration test verifies:
        1. Reservation creation
        2. Duration calculation
        3. Damage report update
        4. Reservation closure
        5. Final state verification
        """
        # Step 1: Create reservation
        reservation = reservation_service.create_reservation(
            mobile_number=sample_customer_data["mobile_number"],
            full_name=sample_customer_data["full_name"],
            license_plate=sample_vehicle_data["license_plate"],
            key_scan_data=sample_vehicle_data["key_scan_data"],
            damage_report="Small scratch on rear bumper",
        )

        # Verify creation
        assert reservation is not None
        assert reservation.status == ReservationStatus.ACTIVE
        assert reservation.qr_code_data is not None

        # Step 2: Calculate current duration
        sleep(0.1)  # Small delay to ensure measurable duration
        duration = reservation_service.calculate_current_duration(reservation.reservation_id)
        assert duration.total_seconds() > 0

        # Step 3: Update vehicle damage
        updated = reservation_service.update_vehicle_damage(
            reservation.reservation_id, "Additional scratch on passenger door"
        )
        assert updated.vehicle.damage_report == "Additional scratch on passenger door"

        # Step 4: Close reservation
        closed = reservation_service.close_reservation(reservation.reservation_id)

        # Step 5: Verify final state
        assert closed.status == ReservationStatus.COMPLETED
        assert closed.check_out_time is not None
        assert closed.parking_duration is not None
        assert closed.check_out_time > closed.check_in_time

        # Verify it's no longer in active reservations
        active_reservations = reservation_service.get_active_reservations()
        active_ids = [r.reservation_id for r in active_reservations]
        assert closed.reservation_id not in active_ids

        # Can still retrieve the closed reservation
        retrieved = reservation_service.get_reservation(closed.reservation_id)
        assert retrieved.status == ReservationStatus.COMPLETED
