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
    status: str = Field(default="open")
    created_at: str = Field(default_factory=lambda: __import__("datetime").datetime.utcnow().isoformat())
    
    @field_validator("created_at")
    @classmethod
    def validate_created_at(cls, v: str) -> str:
        """Validate that created_at is a valid ISO format datetime string."""
        try:
            __import__("datetime").datetime.fromisoformat(v)
        except ValueError:
            raise ValueError("created_at must be a valid ISO format datetime string")
        return v
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
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate that status is one of the allowed values."""
        allowed_statuses = {"open", "closed", "maintenance"}
        if v.lower() not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v.lower()
