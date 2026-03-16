"""Custom exceptions for the valet parking reservation system."""


class ValetParkingError(Exception):
    """Base exception for all valet parking errors."""

    pass


class InvalidReservationError(ValetParkingError):
    """Raised when a reservation operation is invalid."""

    pass


class ReservationNotFoundError(ValetParkingError):
    """Raised when a reservation cannot be found."""

    pass


class ReservationAlreadyClosedError(ValetParkingError):
    """Raised when attempting to close an already closed reservation."""

    pass


class InvalidVehiclePlateError(ValetParkingError):
    """Raised when a vehicle license plate is invalid."""

    pass


class InvalidPhoneNumberError(ValetParkingError):
    """Raised when a phone number is invalid."""

    pass
