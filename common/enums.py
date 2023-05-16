import enum


class StaticEnum(enum.Enum):
    """Static enum class."""

    FMS = "fleet-management-system"
    USERS = "users"
    WEEKDAYS = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    SHIFT_TYPES = ["morning", "afternoon", "evening", "night"]


class ResponseMessages(enum.Enum):
    """Response Messages"""
    INVALID_DATA = "Invalid data"

