"""Data models for parking facilities."""

from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Parking(BaseModel):
    """A parking facility.

    Attributes:
        parking_id: Unique identifier for the parking facility.
        name: Name of the parking facility.
        address: Physical address of the parking facility.
        capacity: Total number of parking spaces.
        floors: Number of floors in the parking facility.
    """

    parking_id: UUID = Field(default_factory=uuid4)
    name: str
    address: str
    capacity: int = Field(gt=0)
    floors: int = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not empty."""
        if not v or not v.strip():
            raise ValueError("Parking name cannot be empty")
        return v.strip()

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        """Validate that address is not empty."""
        if not v or not v.strip():
            raise ValueError("Parking address cannot be empty")
        return v.strip()
