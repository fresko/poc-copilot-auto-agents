"""Tests for QR code generator."""

import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from valet_parking.core.qr_generator import QRCodeGenerator


class TestQRCodeGenerator:
    """Tests for QRCodeGenerator class."""

    def test_generate_qr_data_creates_unique_string(self, qr_generator):
        """Test that QR data generation creates a unique string."""
        reservation_id = uuid4()
        qr_data = qr_generator.generate_qr_data(reservation_id)

        assert isinstance(qr_data, str)
        assert len(qr_data) > 0

    def test_generate_qr_data_contains_reservation_id(self, qr_generator):
        """Test that generated QR data can be decoded to extract reservation ID."""
        reservation_id = uuid4()
        qr_data = qr_generator.generate_qr_data(reservation_id)

        # Should be able to decode it back
        decoded_id = qr_generator.decode_qr_data(qr_data)
        assert decoded_id == reservation_id

    def test_decode_qr_data_extracts_reservation_id(self, qr_generator):
        """Test that QR data decoding extracts the correct reservation ID."""
        reservation_id = uuid4()
        qr_data = qr_generator.generate_qr_data(reservation_id)

        decoded_id = qr_generator.decode_qr_data(qr_data)
        assert decoded_id == reservation_id

    def test_generate_qr_image_creates_file(self, qr_generator):
        """Test that QR image generation creates a file."""
        reservation_id = uuid4()
        qr_data = qr_generator.generate_qr_data(reservation_id)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "qr_code.png"
            qr_generator.generate_qr_image(qr_data, output_path)

            assert output_path.exists()
            assert output_path.stat().st_size > 0

    def test_decode_invalid_qr_data_raises_error(self, qr_generator):
        """Test that decoding invalid QR data raises ValueError."""
        invalid_data = "invalid_base64_data"

        with pytest.raises(ValueError, match="Invalid QR code data"):
            qr_generator.decode_qr_data(invalid_data)

    def test_decode_qr_data_missing_reservation_id_raises_error(self, qr_generator):
        """Test that decoding QR data without reservation_id raises error."""
        import base64
        import json

        # Create valid JSON but without reservation_id
        data = {"type": "valet_parking", "version": "1.0"}
        json_str = json.dumps(data)
        encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")

        with pytest.raises(ValueError, match="reservation_id"):
            qr_generator.decode_qr_data(encoded)
