# Valet Parking Reservation System - Implementation Plan

## Overview
Create a comprehensive valet parking reservation management system in Python that handles ticket creation, vehicle tracking, QR code generation, parking time calculation, and reservation closure. The system will manage the complete lifecycle of a valet parking service from check-in to checkout.

## Requirements

### Functional Requirements
1. **Ticket Creation**: Generate new parking reservations with customer and vehicle information
2. **Customer Data**: Capture mobile number, full name, and license plate scan (KeyScan)
3. **Vehicle Information**: Record license plate number and pre-existing damage documentation
4. **QR Code Generation**: Generate unique QR codes for each reservation for quick retrieval
5. **Time Tracking**: Calculate parking duration from check-in to current time or checkout
6. **Reservation Management**: Support closing/completing reservations with final time calculation
7. **Data Persistence**: Store reservation data for retrieval and audit purposes

### Technical Requirements
1. **Type Safety**: Full type hints using Python 3.14+ syntax
2. **Data Validation**: Use Pydantic models for data validation and serialization
3. **Code Quality**: Adhere to ruff formatting and Google-style docstrings
4. **Testing**: Minimum 80% test coverage on core business logic
5. **Error Handling**: Custom exceptions for business logic errors
6. **Logging**: Comprehensive logging for audit trails

## Architecture Design

### Data Models
The system will use Pydantic models for data validation:

**Customer Information**:
- `mobile_number`: str (validated phone format)
- `full_name`: str (minimum 2 characters)

**Vehicle Information**:
- `license_plate`: str (validated plate format)
- `damage_report`: str | None (optional description of pre-existing damage)
- `key_scan_data`: str | None (scanned key/plate data)

**Reservation**:
- `reservation_id`: UUID (unique identifier)
- `customer`: Customer model
- `vehicle`: Vehicle model
- `check_in_time`: datetime
- `check_out_time`: datetime | None
- `qr_code_data`: str (encoded QR string)
- `status`: Literal["active", "completed", "cancelled"]
- `parking_duration`: timedelta | None (calculated field)

### Core Components
1. **Models Layer** (`src/valet_parking/models/`)
   - Customer, Vehicle, Reservation data models
   - Enums for reservation status

2. **Core Business Logic** (`src/valet_parking/core/`)
   - Reservation service for CRUD operations
   - QR code generator
   - Time calculator
   - Damage documentation handler

3. **Utilities** (`src/valet_parking/utils/`)
   - Validation helpers (phone, plate format)
   - Data formatters
   - QR code utilities

4. **Exceptions** (`src/valet_parking/exceptions.py`)
   - Custom business logic exceptions

5. **Storage** (`src/valet_parking/storage/`)
   - Repository pattern for data persistence
   - In-memory implementation (extendable to database)

## Implementation Steps

### Step 1: Define Custom Exceptions
**File**: `src/valet_parking/exceptions.py`

**Actions**:
- Create base `ValetParkingError` exception
- Create `InvalidReservationError` for invalid reservation operations
- Create `ReservationNotFoundError` for lookup failures
- Create `ReservationAlreadyClosedError` for duplicate closure attempts
- Create `InvalidVehiclePlateError` for plate validation failures
- Create `InvalidPhoneNumberError` for phone validation failures

### Step 2: Create Data Models
**File**: `src/valet_parking/models/reservation.py`

**Actions**:
- Define `ReservationStatus` enum with values: ACTIVE, COMPLETED, CANCELLED
- Create `Customer` Pydantic model with validated fields
- Create `Vehicle` Pydantic model with validated fields
- Create `Reservation` Pydantic model with:
  - Auto-generated UUID
  - Timestamp fields
  - Computed parking duration property
  - QR code data field
  - Status field with default ACTIVE

**File**: `src/valet_parking/models/__init__.py`
- Export all models via `__all__`

### Step 3: Implement Validation Utilities
**File**: `src/valet_parking/utils/validators.py`

**Actions**:
- Implement `validate_phone_number(phone: str) -> bool`
  - Support international formats
  - Raise `InvalidPhoneNumberError` on failure
- Implement `validate_license_plate(plate: str) -> bool`
  - Basic alphanumeric validation
  - Raise `InvalidVehiclePlateError` on failure
- Implement `sanitize_plate_number(plate: str) -> str`
  - Remove special characters, uppercase

**File**: `src/valet_parking/utils/formatters.py`

**Actions**:
- Implement `format_parking_duration(duration: timedelta) -> str`
  - Human-readable format (e.g., "2 hours 30 minutes")
- Implement `format_timestamp(dt: datetime) -> str`
  - ISO format with timezone

### Step 4: Implement QR Code Generator
**File**: `src/valet_parking/core/qr_generator.py`

**Actions**:
- Install dependency: `qrcode` library
- Implement `QRCodeGenerator` class:
  - `generate_qr_data(reservation_id: UUID) -> str`
    - Encode reservation ID and metadata
  - `generate_qr_image(data: str, output_path: Path) -> None`
    - Generate QR code image file
  - `decode_qr_data(qr_data: str) -> UUID`
    - Extract reservation ID from QR data

### Step 5: Implement Time Calculator
**File**: `src/valet_parking/core/time_calculator.py`

**Actions**:
- Implement `TimeCalculator` class:
  - `calculate_duration(check_in: datetime, check_out: datetime | None = None) -> timedelta`
    - If check_out is None, use current time
    - Return time difference
  - `calculate_parking_fee(duration: timedelta, rate_per_hour: float) -> float`
    - Optional: Calculate fees based on duration
    - Support different rate tiers

### Step 6: Implement Repository Pattern
**File**: `src/valet_parking/storage/repository.py`

**Actions**:
- Define `ReservationRepository` Protocol (interface):
  - `save(reservation: Reservation) -> None`
  - `find_by_id(reservation_id: UUID) -> Reservation | None`
  - `find_active_reservations() -> list[Reservation]`
  - `update(reservation: Reservation) -> None`
  - `delete(reservation_id: UUID) -> None`

**File**: `src/valet_parking/storage/in_memory_repository.py`

**Actions**:
- Implement `InMemoryReservationRepository`:
  - Use dict to store reservations by UUID
  - Thread-safe operations (use threading.Lock)
  - Implement all Repository protocol methods

### Step 7: Implement Core Reservation Service
**File**: `src/valet_parking/core/reservation_service.py`

**Actions**:
- Implement `ReservationService` class with dependency injection:
  - Constructor: `__init__(repository: ReservationRepository, qr_generator: QRCodeGenerator, time_calculator: TimeCalculator)`
  
  - `create_reservation(mobile_number: str, full_name: str, license_plate: str, key_scan_data: str | None = None, damage_report: str | None = None) -> Reservation`
    - Validate inputs using validators
    - Create Customer and Vehicle models
    - Generate UUID for reservation
    - Set check_in_time to current time
    - Generate QR code data
    - Create Reservation model with ACTIVE status
    - Save to repository
    - Return reservation
  
  - `get_reservation(reservation_id: UUID) -> Reservation`
    - Fetch from repository
    - Raise `ReservationNotFoundError` if not found
  
  - `get_active_reservations() -> list[Reservation]`
    - Fetch all active reservations
  
  - `calculate_current_duration(reservation_id: UUID) -> timedelta`
    - Get reservation
    - Calculate duration from check_in to now
  
  - `close_reservation(reservation_id: UUID) -> Reservation`
    - Get reservation
    - Check if already closed (raise `ReservationAlreadyClosedError`)
    - Set check_out_time to current time
    - Calculate final parking_duration
    - Update status to COMPLETED
    - Save to repository
    - Return updated reservation
  
  - `update_vehicle_damage(reservation_id: UUID, damage_report: str) -> Reservation`
    - Get reservation
    - Update vehicle damage report
    - Save to repository

### Step 8: Module Initialization
**File**: `src/valet_parking/__init__.py`

**Actions**:
- Import and expose main classes in `__all__`:
  - `ReservationService`
  - `Reservation`, `Customer`, `Vehicle`
  - `ReservationStatus`
  - Custom exceptions

**File**: `src/valet_parking/core/__init__.py`, `src/valet_parking/models/__init__.py`, `src/valet_parking/utils/__init__.py`
- Define `__all__` for each module

### Step 9: Configuration Management (Optional)
**File**: `src/valet_parking/config.py`

**Actions**:
- Create `ValetParkingConfig` using Pydantic BaseSettings:
  - `QR_CODE_VERSION`: int (default: 1)
  - `PARKING_RATE_PER_HOUR`: float (default: 5.0)
  - `TIMEZONE`: str (default: "UTC")
  - Load from environment variables

## Testing Plan

### Test Structure
All tests in `tests/unit/` directory, mirroring source structure.

### Test Files and Cases

#### `tests/unit/models/test_reservation.py`
- `test_customer_creation_valid_data_creates_customer`
- `test_customer_creation_invalid_phone_raises_error`
- `test_vehicle_creation_valid_data_creates_vehicle`
- `test_vehicle_creation_invalid_plate_raises_error`
- `test_reservation_creation_valid_data_creates_reservation`
- `test_reservation_has_unique_id`
- `test_reservation_status_defaults_to_active`
- `test_reservation_parking_duration_calculated_correctly`

#### `tests/unit/utils/test_validators.py`
- `test_validate_phone_number_valid_formats_returns_true`
- `test_validate_phone_number_invalid_format_raises_error`
- `test_validate_license_plate_valid_format_returns_true`
- `test_validate_license_plate_invalid_format_raises_error`
- `test_sanitize_plate_number_removes_special_chars`
- `test_sanitize_plate_number_converts_to_uppercase`

#### `tests/unit/utils/test_formatters.py`
- `test_format_parking_duration_hours_and_minutes`
- `test_format_parking_duration_days_hours_minutes`
- `test_format_timestamp_iso_format`

#### `tests/unit/core/test_qr_generator.py`
- `test_generate_qr_data_creates_unique_string`
- `test_generate_qr_data_contains_reservation_id`
- `test_decode_qr_data_extracts_reservation_id`
- `test_generate_qr_image_creates_file`
- `test_decode_invalid_qr_data_raises_error`

#### `tests/unit/core/test_time_calculator.py`
- `test_calculate_duration_with_checkout_returns_difference`
- `test_calculate_duration_without_checkout_uses_current_time`
- `test_calculate_duration_handles_same_time`
- `test_calculate_parking_fee_correct_calculation`
- `test_calculate_parking_fee_rounds_up_partial_hours`

#### `tests/unit/storage/test_in_memory_repository.py`
- `test_save_reservation_stores_correctly`
- `test_find_by_id_existing_reservation_returns_reservation`
- `test_find_by_id_nonexistent_returns_none`
- `test_update_reservation_modifies_existing`
- `test_delete_reservation_removes_from_storage`
- `test_find_active_reservations_returns_only_active`
- `test_repository_thread_safe_concurrent_writes`

#### `tests/unit/core/test_reservation_service.py`
- `test_create_reservation_valid_data_creates_and_saves`
- `test_create_reservation_generates_qr_code`
- `test_create_reservation_invalid_phone_raises_error`
- `test_create_reservation_invalid_plate_raises_error`
- `test_get_reservation_existing_returns_reservation`
- `test_get_reservation_nonexistent_raises_error`
- `test_close_reservation_sets_checkout_time`
- `test_close_reservation_updates_status_to_completed`
- `test_close_reservation_already_closed_raises_error`
- `test_calculate_current_duration_returns_time_elapsed`
- `test_update_vehicle_damage_modifies_damage_report`
- `test_get_active_reservations_returns_active_only`

#### `tests/conftest.py`
**Shared Fixtures**:
- `repository`: Returns InMemoryReservationRepository instance
- `qr_generator`: Returns QRCodeGenerator instance
- `time_calculator`: Returns TimeCalculator instance
- `reservation_service`: Returns configured ReservationService
- `sample_customer_data`: Dict with valid customer data
- `sample_vehicle_data`: Dict with valid vehicle data
- `sample_reservation`: Pre-created Reservation for testing

### Integration Tests (Optional)
**File**: `tests/integration/test_reservation_flow.py`
- `test_complete_reservation_lifecycle`
  - Create reservation
  - Calculate duration
  - Update damage
  - Close reservation
  - Verify final state

## Dependencies

Add to `pyproject.toml`:
```toml
[project]
dependencies = [
    "pydantic>=2.0",
    "qrcode[pil]>=7.4",
    "python-dateutil>=2.8",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-mock>=3.10",
    "mypy>=1.0",
    "ruff>=0.1",
]
```

## Implementation Order

1. **Phase 1 - Foundation** (Days 1-2)
   - Exceptions
   - Data models
   - Validators

2. **Phase 2 - Utilities** (Days 3-4)
   - QR code generator
   - Time calculator
   - Formatters

3. **Phase 3 - Storage** (Day 5)
   - Repository interface
   - In-memory implementation

4. **Phase 4 - Core Service** (Days 6-7)
   - Reservation service
   - Integration with all components

5. **Phase 5 - Testing** (Days 8-9)
   - Unit tests for all components
   - Integration tests
   - Achieve 80%+ coverage

6. **Phase 6 - Documentation** (Day 10)
   - API documentation
   - Usage examples
   - README updates

## Usage Example

```python
from valet_parking import ReservationService
from valet_parking.storage import InMemoryReservationRepository
from valet_parking.core import QRCodeGenerator, TimeCalculator

# Setup
repository = InMemoryReservationRepository()
qr_generator = QRCodeGenerator()
time_calculator = TimeCalculator()
service = ReservationService(repository, qr_generator, time_calculator)

# Create new reservation
reservation = service.create_reservation(
    mobile_number="+1-555-0123",
    full_name="John Doe",
    license_plate="ABC123",
    key_scan_data="KEY_SCAN_DATA_HERE",
    damage_report="Small scratch on rear bumper"
)

print(f"Reservation ID: {reservation.reservation_id}")
print(f"QR Code: {reservation.qr_code_data}")

# Check parking duration
from time import sleep
sleep(5)  # Simulate parking time
duration = service.calculate_current_duration(reservation.reservation_id)
print(f"Current duration: {duration}")

# Close reservation
closed = service.close_reservation(reservation.reservation_id)
print(f"Final duration: {closed.parking_duration}")
print(f"Status: {closed.status}")
```

## Security Considerations

1. **Personal Data**: Customer phone numbers and names should be handled according to privacy regulations (GDPR, CCPA)
2. **QR Code Security**: Consider encrypting reservation data in QR codes
3. **Access Control**: Implement authentication/authorization for service access
4. **Audit Logging**: Log all reservation operations with timestamps
5. **Data Retention**: Define policy for how long to retain closed reservations

## Future Enhancements

1. **Database Integration**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Image Storage**: Store photos of vehicle damage
3. **Payment Integration**: Calculate and process parking fees
4. **API Layer**: REST API using FastAPI for external access
5. **SMS Notifications**: Send QR codes and updates via SMS
6. **Web Interface**: Admin dashboard for valet attendants
7. **Analytics**: Reporting on parking patterns and revenue
8. **Multi-location Support**: Handle multiple parking locations

## Validation Checklist

Before considering implementation complete:
- [ ] All unit tests passing with 80%+ coverage
- [ ] Type checking passes with mypy
- [ ] Code formatted with ruff
- [ ] All docstrings present and complete
- [ ] Integration tests demonstrate full workflow
- [ ] Error cases properly handled and tested
- [ ] Logging implemented for audit trail
- [ ] README with usage examples
- [ ] Dependencies documented in pyproject.toml

## Commands to Run After Implementation

```bash
# Install dependencies
pip install -e ".[dev]"

# Format code
ruff check --fix .
ruff format .

# Type check
mypy src/valet_parking/

# Run tests with coverage
pytest tests/ -v --cov=src/valet_parking --cov-report=html

# Run all quality checks
ruff check . && mypy src/ && pytest
```

---

**Document Version**: 1.0  
**Date**: March 16, 2026  
**Status**: Ready for Implementation