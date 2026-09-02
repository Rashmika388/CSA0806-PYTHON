from collections import defaultdict
from statistics import mean


def calculate_distance(start_odometer, end_odometer):
    """Calculate distance travelled."""

    return float(end_odometer) - float(start_odometer)


def calculate_mileage(distance, fuel_consumed):
    """Calculate mileage in km/L."""

    distance = float(distance)
    fuel_consumed = float(fuel_consumed)

    if fuel_consumed <= 0:
        return 0

    return distance / fuel_consumed


def calculate_fuel_cost(fuel_consumed, fuel_price):
    """Calculate total fuel cost."""

    return float(fuel_consumed) * float(fuel_price)


def group_trips_by_vehicle(trips):
    """
    Group trip records using a dictionary.
    Result:
    {
        vehicle_number: [trip1, trip2, ...]
    }
    """

    grouped = defaultdict(list)

    for trip in trips:
        grouped[trip["vehicle_no"]].append(trip)

    return dict(grouped)


def get_unique_vehicles(trips):
    """Return unique vehicle numbers using a set."""

    vehicles = set()

    for trip in trips:
        vehicles.add(trip["vehicle_no"])

    return vehicles


def find_duplicate_trip_ids(trips):
    """Find duplicate trip IDs using a set."""

    seen = set()
    duplicates = set()

    for trip in trips:
        trip_id = trip["trip_id"]

        if trip_id in seen:
            duplicates.add(trip_id)
        else:
            seen.add(trip_id)

    return duplicates


def remove_duplicate_trips(trips):
    """
    Remove duplicate trip records.

    A tuple is used as a unique key for each record.
    """

    unique_trips = []
    seen = set()

    for trip in trips:

        key = (
            trip["vehicle_no"],
            trip["date"],
            trip["start_odometer"],
            trip["end_odometer"],
            trip["fuel_consumed"]
        )

        if key not in seen:
            seen.add(key)
            unique_trips.append(trip)

    return unique_trips


def create_vehicle_summary_tuple(vehicle_no, distance, fuel, mileage, cost):
    """
    Create a tuple containing summary information.

    This explicitly demonstrates tuple usage.
    """

    return (
        vehicle_no,
        distance,
        fuel,
        mileage,
        cost
    )


def vehicle_mileage_summary(trips):
    """Calculate mileage summary for every vehicle."""

    grouped = group_trips_by_vehicle(trips)

    summary = {}

    for vehicle_no, vehicle_trips in grouped.items():

        total_distance_value = 0
        total_fuel_value = 0
        total_cost_value = 0

        for trip in vehicle_trips:

            distance = float(trip["distance"])
            fuel = float(trip["fuel_consumed"])
            cost = float(trip["fuel_cost"])

            total_distance_value += distance
            total_fuel_value += fuel
            total_cost_value += cost

        mileage = calculate_mileage(
            total_distance_value,
            total_fuel_value
        )

        summary[vehicle_no] = {
            "distance": total_distance_value,
            "fuel": total_fuel_value,
            "mileage": mileage,
            "cost": total_cost_value
        }

    return summary


def rank_vehicles_by_efficiency(trips):
    """Rank vehicles from highest to lowest mileage."""

    summary = vehicle_mileage_summary(trips)

    ranking = list(summary.items())

    ranking.sort(
        key=lambda item: item[1]["mileage"],
        reverse=True
    )

    return ranking


def calculate_monthly_consumption(trips):
    """Group fuel consumption by month."""

    monthly = defaultdict(
        lambda: {
            "distance": 0,
            "fuel": 0,
            "cost": 0
        }
    )

    for trip in trips:

        month = trip["date"][:7]

        monthly[month]["distance"] += float(
            trip["distance"]
        )

        monthly[month]["fuel"] += float(
            trip["fuel_consumed"]
        )

        monthly[month]["cost"] += float(
            trip["fuel_cost"]
        )

    return dict(monthly)


def calculate_average_monthly_consumption(trips):
    """Calculate average fuel consumed per month."""

    monthly = calculate_monthly_consumption(trips)

    if not monthly:
        return 0

    fuel_values = [
        data["fuel"]
        for data in monthly.values()
    ]

    return mean(fuel_values)


def find_abnormal_trips(trips, threshold=10):
    """
    Find trips with low mileage.

    Low mileage means unusually high fuel consumption.
    Default threshold = 10 km/L.
    """

    abnormal = []

    for trip in trips:

        distance = float(trip["distance"])
        fuel = float(trip["fuel_consumed"])

        mileage = calculate_mileage(
            distance,
            fuel
        )

        if mileage < threshold:

            trip_copy = trip.copy()
            trip_copy["mileage"] = mileage

            abnormal.append(trip_copy)

    return abnormal


def total_fuel_consumed(trips):
    """Calculate total fuel consumed."""

    return sum(
        float(trip["fuel_consumed"])
        for trip in trips
    )


def total_distance(trips):
    """Calculate total distance."""

    return sum(
        float(trip["distance"])
        for trip in trips
    )


def total_fuel_cost(trips):
    """Calculate total fuel cost."""

    return sum(
        float(trip["fuel_cost"])
        for trip in trips
    )