"""Configuration settings for valet parking system."""

from pydantic_settings import BaseSettings


class ValetParkingConfig(BaseSettings):
    """Configuration settings for valet parking system.

    Attributes:
        qr_code_version: QR code version number.
        parking_rate_per_hour: Hourly parking rate in currency units.
        timezone: Timezone for timestamp operations.
    """

    qr_code_version: int = 1
    parking_rate_per_hour: float = 5.0
    timezone: str = "UTC"

    class Config:
        """Pydantic configuration."""

        env_prefix = "VALET_"
