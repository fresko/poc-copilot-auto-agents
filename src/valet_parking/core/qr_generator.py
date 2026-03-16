"""QR code generation and decoding for reservations."""

import base64
import json
from pathlib import Path
from uuid import UUID

import qrcode


class QRCodeGenerator:
    """Generate and decode QR codes for parking reservations.

    QR codes encode the reservation ID and metadata for quick retrieval.
    """

    def generate_qr_data(self, reservation_id: UUID) -> str:
        """Generate QR code data string from reservation ID.

        Args:
            reservation_id: Unique reservation identifier.

        Returns:
            Base64 encoded JSON string containing reservation data.

        Examples:
            >>> generator = QRCodeGenerator()
            >>> qr_data = generator.generate_qr_data(uuid4())
            >>> isinstance(qr_data, str)
            True
        """
        data = {
            "reservation_id": str(reservation_id),
            "type": "valet_parking",
            "version": "1.0",
        }

        json_str = json.dumps(data)
        encoded = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
        return encoded

    def generate_qr_image(self, data: str, output_path: Path) -> None:
        """Generate QR code image file from data string.

        Args:
            data: QR code data string to encode.
            output_path: Path where QR code image will be saved.

        Examples:
            >>> generator = QRCodeGenerator()
            >>> qr_data = generator.generate_qr_data(uuid4())
            >>> generator.generate_qr_image(qr_data, Path("qr.png"))
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(str(output_path))

    def decode_qr_data(self, qr_data: str) -> UUID:
        """Extract reservation ID from QR code data.

        Args:
            qr_data: Base64 encoded QR code data string.

        Returns:
            Reservation UUID extracted from QR data.

        Raises:
            ValueError: If QR data is invalid or malformed.

        Examples:
            >>> generator = QRCodeGenerator()
            >>> reservation_id = uuid4()
            >>> qr_data = generator.generate_qr_data(reservation_id)
            >>> decoded_id = generator.decode_qr_data(qr_data)
            >>> decoded_id == reservation_id
            True
        """
        try:
            decoded_bytes = base64.b64decode(qr_data.encode("utf-8"))
            json_str = decoded_bytes.decode("utf-8")
            data = json.loads(json_str)

            if "reservation_id" not in data:
                raise ValueError("QR data missing reservation_id field")

            return UUID(data["reservation_id"])

        except (json.JSONDecodeError, ValueError, KeyError) as e:
            raise ValueError(f"Invalid QR code data: {e}") from e
