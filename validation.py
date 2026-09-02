import re
from datetime import datetime


def clean_text(value):
    """Remove unnecessary spaces from user input."""
    return str(value).strip()


def validate_vehicle_number(vehicle_no):
    """
    Validate and standardize an Indian-style vehicle number.
    Example: TN01AB1234
    """
    vehicle_no = clean_text(vehicle_no).upper()

    pattern = r"^[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{1,4}$"

    if re.fullmatch(pattern, vehicle_no):
        return vehicle_no

    return None


def validate_date(date_text):
    """Validate date in YYYY-MM-DD format."""
    date_text = clean_text(date_text)

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        return None


def validate_positive_number(value, field_name):
    """Validate a number greater than zero."""
    try:
        number = float(value)

        if number <= 0:
            print(f"{field_name} must be greater than 0.")
            return None

        return number

    except ValueError:
        print(f"{field_name} must be a valid number.")
        return None


def validate_non_negative_number(value, field_name):
    """Validate a number greater than or equal to zero."""
    try:
        number = float(value)

        if number < 0:
            print(f"{field_name} cannot be negative.")
            return None

        return number

    except ValueError:
        print(f"{field_name} must be a valid number.")
        return None


def validate_fuel_type(fuel_type):
    """Validate supported fuel types."""
    fuel_type = clean_text(fuel_type).capitalize()

    allowed_types = {
        "Petrol",
        "Diesel",
        "Cng",
        "Electric"
    }

    if fuel_type in allowed_types:
        if fuel_type == "Cng":
            return "CNG"

        return fuel_type

    return None