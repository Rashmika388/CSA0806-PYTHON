import csv
import os


VEHICLE_FILE = "vehicles.csv"
TRIP_FILE = "trips.csv"


VEHICLE_FIELDS = [
    "vehicle_no",
    "model",
    "fuel_type",
    "registration_date"
]


TRIP_FIELDS = [
    "trip_id",
    "vehicle_no",
    "date",
    "start_odometer",
    "end_odometer",
    "distance",
    "fuel_consumed",
    "fuel_price",
    "fuel_cost"
]


def initialize_files():
    """Create CSV files and headers if they do not exist."""

    if not os.path.exists(VEHICLE_FILE):
        with open(
            VEHICLE_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=VEHICLE_FIELDS
            )

            writer.writeheader()

    if not os.path.exists(TRIP_FILE):
        with open(
            TRIP_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=TRIP_FIELDS
            )

            writer.writeheader()


def load_vehicles():
    """Read vehicle records from CSV."""

    initialize_files()

    try:
        with open(
            VEHICLE_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            return list(csv.DictReader(file))

    except FileNotFoundError:
        return []


def save_vehicle(vehicle):
    """Save a vehicle record."""

    initialize_files()

    with open(
        VEHICLE_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=VEHICLE_FIELDS
        )

        writer.writerow(vehicle)


def load_trips():
    """Read trip records from CSV."""

    initialize_files()

    try:
        with open(
            TRIP_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            return list(csv.DictReader(file))

    except FileNotFoundError:
        return []


def save_trip(trip):
    """Save a trip record."""

    initialize_files()

    with open(
        TRIP_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=TRIP_FIELDS
        )

        writer.writerow(trip)


def get_next_trip_id():
    """Generate the next available trip ID."""

    trips = load_trips()

    if not trips:
        return 1

    ids = []

    for trip in trips:
        try:
            ids.append(int(trip["trip_id"]))
        except (ValueError, KeyError):
            continue

    if not ids:
        return 1

    return max(ids) + 1