from analysis import (
    vehicle_mileage_summary,
    calculate_monthly_consumption,
    calculate_average_monthly_consumption,
    find_abnormal_trips,
    rank_vehicles_by_efficiency,
    total_fuel_consumed,
    total_distance,
    total_fuel_cost,
    get_unique_vehicles,
    find_duplicate_trip_ids,
    create_vehicle_summary_tuple
)


def display_vehicle_summary(trips):
    """Display vehicle-wise fuel efficiency."""

    summary = vehicle_mileage_summary(trips)

    if not summary:
        print("\nNo trip records available.")
        return

    print("\n" + "=" * 75)
    print("VEHICLE FUEL EFFICIENCY SUMMARY")
    print("=" * 75)

    print(
        f"{'Vehicle':<15}"
        f"{'Distance':<15}"
        f"{'Fuel':<12}"
        f"{'Mileage':<12}"
        f"{'Cost':<15}"
    )

    print("-" * 75)

    for vehicle_no, data in summary.items():

        print(
            f"{vehicle_no:<15}"
            f"{data['distance']:<15.2f}"
            f"{data['fuel']:<12.2f}"
            f"{data['mileage']:<12.2f}"
            f"₹{data['cost']:<14.2f}"
        )


def display_monthly_report(trips):
    """Display monthly fuel consumption."""

    monthly = calculate_monthly_consumption(trips)

    if not monthly:
        print("\nNo trip records available.")
        return

    print("\n" + "=" * 75)
    print("MONTHLY FUEL CONSUMPTION REPORT")
    print("=" * 75)

    print(
        f"{'Month':<12}"
        f"{'Distance (km)':<20}"
        f"{'Fuel (L)':<15}"
        f"{'Cost (₹)':<15}"
    )

    print("-" * 75)

    for month, data in sorted(monthly.items()):

        print(
            f"{month:<12}"
            f"{data['distance']:<20.2f}"
            f"{data['fuel']:<15.2f}"
            f"{data['cost']:<15.2f}"
        )

    average = calculate_average_monthly_consumption(trips)

    print("\nAverage Monthly Fuel Consumption:")
    print(f"{average:.2f} L")


def display_abnormal_trips(trips, threshold=10):
    """Display high-consumption trips."""

    abnormal = find_abnormal_trips(
        trips,
        threshold
    )

    print("\n" + "=" * 80)
    print("ABNORMAL / HIGH-CONSUMPTION TRIPS")
    print("=" * 80)

    print(
        f"Trips with mileage below {threshold} km/L are considered abnormal."
    )

    if not abnormal:
        print("\nNo abnormal trips detected.")
        return

    print()

    for trip in abnormal:

        print(
            f"Trip ID: {trip['trip_id']} | "
            f"Vehicle: {trip['vehicle_no']} | "
            f"Distance: {float(trip['distance']):.2f} km | "
            f"Fuel: {float(trip['fuel_consumed']):.2f} L | "
            f"Mileage: {trip['mileage']:.2f} km/L"
        )


def generate_consolidated_report(trips):
    """Generate complete project report."""

    print("\n")
    print("=" * 80)
    print("              CONSOLIDATED VEHICLE FUEL REPORT")
    print("=" * 80)

    if not trips:
        print("\nNo trip records available.")
        return

    total_trips = len(trips)
    unique_vehicles = len(get_unique_vehicles(trips))

    distance = total_distance(trips)
    fuel = total_fuel_consumed(trips)
    cost = total_fuel_cost(trips)

    print(f"\nTotal Trips          : {total_trips}")
    print(f"Unique Vehicles      : {unique_vehicles}")
    print(f"Total Distance       : {distance:.2f} km")
    print(f"Total Fuel Consumed  : {fuel:.2f} L")
    print(f"Total Fuel Cost      : ₹{cost:.2f}")

    ranking = rank_vehicles_by_efficiency(trips)

    if ranking:

        print("\n" + "-" * 80)
        print("VEHICLE EFFICIENCY RANKING")
        print("-" * 80)

        for position, (vehicle_no, data) in enumerate(
            ranking,
            start=1
        ):

            print(
                f"{position}. "
                f"{vehicle_no} - "
                f"{data['mileage']:.2f} km/L"
            )

        most_efficient = ranking[0]
        least_efficient = ranking[-1]

        print("\n" + "-" * 80)
        print("MOST EFFICIENT VEHICLE")
        print("-" * 80)

        print(
            f"Vehicle : {most_efficient[0]}"
        )

        print(
            f"Mileage : "
            f"{most_efficient[1]['mileage']:.2f} km/L"
        )

        print("\n" + "-" * 80)
        print("LEAST EFFICIENT VEHICLE")
        print("-" * 80)

        print(
            f"Vehicle : {least_efficient[0]}"
        )

        print(
            f"Mileage : "
            f"{least_efficient[1]['mileage']:.2f} km/L"
        )

    abnormal = find_abnormal_trips(trips)

    print("\n" + "-" * 80)
    print("ABNORMAL TRIP ANALYSIS")
    print("-" * 80)

    if abnormal:

        print(
            f"Number of abnormal trips: "
            f"{len(abnormal)}"
        )

        for trip in abnormal:

            print(
                f"Trip {trip['trip_id']} - "
                f"{trip['vehicle_no']} - "
                f"{trip['mileage']:.2f} km/L"
            )

    else:
        print("No abnormal trips detected.")

    duplicates = find_duplicate_trip_ids(trips)

    print("\n" + "-" * 80)
    print("DUPLICATE TRIP ID ANALYSIS")
    print("-" * 80)

    if duplicates:
        print(
            "Duplicate Trip IDs:",
            ", ".join(sorted(duplicates))
        )
    else:
        print("No duplicate trip IDs found.")

    print("\n" + "-" * 80)
    print("TUPLE-BASED VEHICLE SUMMARY")
    print("-" * 80)

    if ranking:

        vehicle_no, data = ranking[0]

        summary_tuple = create_vehicle_summary_tuple(
            vehicle_no,
            data["distance"],
            data["fuel"],
            data["mileage"],
            data["cost"]
        )

        print("Summary tuple:")
        print(summary_tuple)

    print("\n" + "=" * 80)
    print("                    END OF REPORT")
    print("=" * 80)