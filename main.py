from validation import (
    validate_vehicle_number,
    validate_date,
    validate_positive_number,
    validate_fuel_type
)

from data_access import (
    initialize_files,
    load_vehicles,
    save_vehicle,
    load_trips,
    save_trip,
    get_next_trip_id
)

from analysis import (
    calculate_distance,
    calculate_mileage,
    calculate_fuel_cost,
    vehicle_mileage_summary,
    calculate_monthly_consumption,
    rank_vehicles_by_efficiency,
    find_abnormal_trips,
    total_fuel_consumed,
    total_distance,
    total_fuel_cost
)

from reports import (
    display_vehicle_summary,
    display_monthly_report,
    display_abnormal_trips,
    generate_consolidated_report
)


def print_header(title):
    """Display a formatted section heading."""

    print("\n")
    print("=" * 70)
    print(title.center(70))
    print("=" * 70)


def register_vehicle():
    """Register a new vehicle."""

    print_header("REGISTER VEHICLE")

    vehicle_no = input("Enter vehicle number: ")
    vehicle_no = validate_vehicle_number(vehicle_no)

    if vehicle_no is None:
        print("Invalid vehicle number.")
        print("Example: TN01AB1234")
        return

    vehicles = load_vehicles()

    for vehicle in vehicles:

        if vehicle["vehicle_no"] == vehicle_no:

            print("This vehicle is already registered.")
            return

    model = input("Enter vehicle model: ").strip()

    if not model:
        print("Vehicle model cannot be empty.")
        return

    fuel_type = input(
        "Enter fuel type (Petrol/Diesel/CNG/Electric): "
    )

    fuel_type = validate_fuel_type(fuel_type)

    if fuel_type is None:
        print("Invalid fuel type.")
        return

    registration_date = input(
        "Enter registration date (YYYY-MM-DD): "
    )

    registration_date = validate_date(
        registration_date
    )

    if registration_date is None:
        print("Invalid date.")
        return

    vehicle = {
        "vehicle_no": vehicle_no,
        "model": model,
        "fuel_type": fuel_type,
        "registration_date": registration_date
    }

    save_vehicle(vehicle)

    print("\nVehicle registered successfully!")


def view_vehicles():
    """Display all registered vehicles."""

    print_header("REGISTERED VEHICLES")

    vehicles = load_vehicles()

    if not vehicles:
        print("No vehicles registered.")
        return

    print(
        f"{'Vehicle No.':<18}"
        f"{'Model':<18}"
        f"{'Fuel Type':<15}"
        f"{'Registration Date':<20}"
    )

    print("-" * 70)

    for vehicle in vehicles:

        print(
            f"{vehicle['vehicle_no']:<18}"
            f"{vehicle['model']:<18}"
            f"{vehicle['fuel_type']:<15}"
            f"{vehicle['registration_date']:<20}"
        )


def add_trip():
    """Add a trip and fuel entry."""

    print_header("ADD TRIP / FUEL ENTRY")

    vehicles = load_vehicles()

    if not vehicles:
        print("No vehicles are registered.")
        print("Please register a vehicle first.")
        return

    vehicle_no = input("Enter vehicle number: ")

    vehicle_no = validate_vehicle_number(
        vehicle_no
    )

    if vehicle_no is None:
        print("Invalid vehicle number.")
        return

    registered_numbers = {
        vehicle["vehicle_no"]
        for vehicle in vehicles
    }

    if vehicle_no not in registered_numbers:
        print("Vehicle is not registered.")
        return

    date = input(
        "Enter trip date (YYYY-MM-DD): "
    )

    date = validate_date(date)

    if date is None:
        print("Invalid date.")
        return

    start_odometer = validate_positive_number(
        input("Enter starting odometer reading: "),
        "Starting odometer"
    )

    if start_odometer is None:
        return

    end_odometer = validate_positive_number(
        input("Enter ending odometer reading: "),
        "Ending odometer"
    )

    if end_odometer is None:
        return

    if end_odometer <= start_odometer:
        print(
            "Ending odometer must be greater "
            "than starting odometer."
        )
        return

    fuel_consumed = validate_positive_number(
        input("Enter fuel consumed (litres): "),
        "Fuel consumed"
    )

    if fuel_consumed is None:
        return

    fuel_price = validate_positive_number(
        input("Enter fuel price per litre (₹): "),
        "Fuel price"
    )

    if fuel_price is None:
        return

    distance = calculate_distance(
        start_odometer,
        end_odometer
    )

    mileage = calculate_mileage(
        distance,
        fuel_consumed
    )

    fuel_cost = calculate_fuel_cost(
        fuel_consumed,
        fuel_price
    )

    trip_id = get_next_trip_id()

    trip = {
        "trip_id": str(trip_id),
        "vehicle_no": vehicle_no,
        "date": date,
        "start_odometer": f"{start_odometer:.2f}",
        "end_odometer": f"{end_odometer:.2f}",
        "distance": f"{distance:.2f}",
        "fuel_consumed": f"{fuel_consumed:.2f}",
        "fuel_price": f"{fuel_price:.2f}",
        "fuel_cost": f"{fuel_cost:.2f}"
    }

    save_trip(trip)

    print("\nTrip saved successfully!")

    print(f"Trip ID       : {trip_id}")
    print(f"Distance      : {distance:.2f} km")
    print(f"Mileage       : {mileage:.2f} km/L")
    print(f"Fuel Cost     : ₹{fuel_cost:.2f}")


def view_trips():
    """Display all trip records."""

    print_header("TRIP RECORDS")

    trips = load_trips()

    if not trips:
        print("No trip records available.")
        return

    print(
        f"{'ID':<6}"
        f"{'Vehicle':<15}"
        f"{'Date':<13}"
        f"{'Distance':<14}"
        f"{'Fuel':<12}"
        f"{'Mileage':<12}"
        f"{'Cost':<12}"
    )

    print("-" * 85)

    for trip in trips:

        distance = float(trip["distance"])
        fuel = float(trip["fuel_consumed"])

        mileage = calculate_mileage(
            distance,
            fuel
        )

        print(
            f"{trip['trip_id']:<6}"
            f"{trip['vehicle_no']:<15}"
            f"{trip['date']:<13}"
            f"{distance:<14.2f}"
            f"{fuel:<12.2f}"
            f"{mileage:<12.2f}"
            f"₹{float(trip['fuel_cost']):<11.2f}"
        )


def show_mileage():
    """Display vehicle mileage summary."""

    print_header("VEHICLE MILEAGE")

    trips = load_trips()

    display_vehicle_summary(trips)


def show_monthly_consumption():
    """Display monthly fuel consumption."""

    print_header("MONTHLY FUEL CONSUMPTION")

    trips = load_trips()

    display_monthly_report(trips)


def show_fuel_cost():
    """Display fuel cost analysis."""

    print_header("FUEL COST ANALYSIS")

    trips = load_trips()

    if not trips:
        print("No trip records available.")
        return

    fuel = total_fuel_consumed(trips)
    cost = total_fuel_cost(trips)
    distance = total_distance(trips)

    print(f"Total Distance      : {distance:.2f} km")
    print(f"Total Fuel Consumed : {fuel:.2f} L")
    print(f"Total Fuel Cost     : ₹{cost:.2f}")

    if fuel > 0:
        print(
            f"Average Fuel Price : "
            f"₹{cost / fuel:.2f} per litre"
        )


def show_ranking():
    """Display vehicle efficiency ranking."""

    print_header("VEHICLE EFFICIENCY RANKING")

    trips = load_trips()

    ranking = rank_vehicles_by_efficiency(
        trips
    )

    if not ranking:
        print("No trip records available.")
        return

    for position, (vehicle_no, data) in enumerate(
        ranking,
        start=1
    ):

        print(
            f"{position}. "
            f"{vehicle_no} - "
            f"{data['mileage']:.2f} km/L"
        )


def show_abnormal_trips():
    """Display abnormal/high-consumption trips."""

    print_header("ABNORMAL TRIP DETECTION")

    trips = load_trips()

    display_abnormal_trips(
        trips,
        threshold=10
    )


def show_data_summary():
    """Display basic data summary."""

    print_header("DATA SUMMARY")

    vehicles = load_vehicles()
    trips = load_trips()

    unique_vehicles = {
        vehicle["vehicle_no"]
        for vehicle in vehicles
    }

    print(
        f"Registered Vehicles : "
        f"{len(unique_vehicles)}"
    )

    print(
        f"Total Trip Records  : "
        f"{len(trips)}"
    )

    print(
        f"Total Distance      : "
        f"{total_distance(trips):.2f} km"
    )

    print(
        f"Total Fuel          : "
        f"{total_fuel_consumed(trips):.2f} L"
    )

    print(
        f"Total Fuel Cost     : "
        f"₹{total_fuel_cost(trips):.2f}"
    )


def show_report():
    """Generate consolidated report."""

    trips = load_trips()

    generate_consolidated_report(
        trips
    )


def main():
    """Main menu-driven application."""

    initialize_files()

    while True:

        print("\n")
        print("=" * 70)
        print("          VEHICLE FUEL MANAGEMENT SYSTEM")
        print("=" * 70)

        print("1. Register Vehicle")
        print("2. View Vehicles")
        print("3. Add Trip / Fuel Entry")
        print("4. View Trip Records")
        print("5. Calculate Vehicle Mileage")
        print("6. Monthly Fuel Consumption")
        print("7. Fuel Cost Analysis")
        print("8. Vehicle Efficiency Ranking")
        print("9. Detect Abnormal Trips")
        print("10. Data Summary")
        print("11. Generate Consolidated Report")
        print("12. Exit")

        print("=" * 70)

        choice = input(
            "Enter your choice (1-12): "
        ).strip()

        if choice == "1":
            register_vehicle()

        elif choice == "2":
            view_vehicles()

        elif choice == "3":
            add_trip()

        elif choice == "4":
            view_trips()

        elif choice == "5":
            show_mileage()

        elif choice == "6":
            show_monthly_consumption()

        elif choice == "7":
            show_fuel_cost()

        elif choice == "8":
            show_ranking()

        elif choice == "9":
            show_abnormal_trips()

        elif choice == "10":
            show_data_summary()

        elif choice == "11":
            show_report()

        elif choice == "12":
            print("\nThank you for using the Vehicle Fuel Management System!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 12.")


if __name__ == "__main__":
    main()