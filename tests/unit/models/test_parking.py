"""Tests for Parking model."""

import pytest

from valet_parking.models.parking import Parking


class TestParking:
    """Tests for Parking model."""

    def test_parking_creation_valid_data_creates_parking(self):
        """Test that valid data creates a parking facility successfully."""
        parking = Parking(name="City Center Parking", address="123 Main St", capacity=200, floors=4)

        assert parking.name == "City Center Parking"
        assert parking.address == "123 Main St"
        assert parking.capacity == 200
        assert parking.floors == 4

    def test_parking_has_unique_id(self):
        """Test that each parking facility gets a unique ID."""
        parking1 = Parking(name="Parking A", address="1 A St", capacity=100, floors=2)
        parking2 = Parking(name="Parking B", address="2 B St", capacity=50, floors=1)

        assert parking1.parking_id != parking2.parking_id

    def test_parking_name_strips_whitespace(self):
        """Test that name is stripped of whitespace."""
        parking = Parking(name="  Downtown Parking  ", address="456 Oak Ave", capacity=50, floors=2)

        assert parking.name == "Downtown Parking"

    def test_parking_address_strips_whitespace(self):
        """Test that address is stripped of whitespace."""
        parking = Parking(name="Airport Parking", address="  789 Airport Rd  ", capacity=500, floors=5)

        assert parking.address == "789 Airport Rd"

    def test_parking_empty_name_raises_error(self):
        """Test that empty name raises validation error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Parking(name="", address="123 Main St", capacity=100, floors=2)

    def test_parking_empty_address_raises_error(self):
        """Test that empty address raises validation error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Parking(name="City Parking", address="", capacity=100, floors=2)

    def test_parking_zero_capacity_raises_error(self):
        """Test that zero capacity raises validation error."""
        with pytest.raises(ValueError):
            Parking(name="City Parking", address="123 Main St", capacity=0, floors=2)

    def test_parking_negative_capacity_raises_error(self):
        """Test that negative capacity raises validation error."""
        with pytest.raises(ValueError):
            Parking(name="City Parking", address="123 Main St", capacity=-10, floors=2)

    def test_parking_zero_floors_raises_error(self):
        """Test that zero floors raises validation error."""
        with pytest.raises(ValueError):
            Parking(name="City Parking", address="123 Main St", capacity=100, floors=0)

    def test_parking_negative_floors_raises_error(self):
        """Test that negative floors raises validation error."""
        with pytest.raises(ValueError):
            Parking(name="City Parking", address="123 Main St", capacity=100, floors=-1)
