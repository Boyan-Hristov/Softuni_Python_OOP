from project.route import Route
from project.user import User
from project.vehicles.cargo_van import CargoVan
from project.vehicles.passenger_car import PassengerCar


class ManagingApp:
    VALID_VEHICLES = {"PassengerCar": PassengerCar, "CargoVan": CargoVan}

    def __init__(self):
        self.users = []
        self.vehicles = []
        self.routes = []

    def register_user(self, first_name: str, last_name: str, driving_license_number: str):
        try:
            next(filter(lambda u: u.driving_license_number == driving_license_number, self.users))
        except StopIteration:
            user = User(first_name, last_name, driving_license_number)
            self.users.append(user)
            return f"{first_name} {last_name} was successfully registered under DLN-{driving_license_number}"

        return f"{driving_license_number} has already been registered to our platform."

    def upload_vehicle(self, vehicle_type: str, brand: str, model: str, license_plate_number: str):
        if vehicle_type not in ManagingApp.VALID_VEHICLES.keys():
            return f"Vehicle type {vehicle_type} is inaccessible."

        try:
            next(filter(lambda v: v.license_plate_number == license_plate_number, self.vehicles))
        except StopIteration:
            vehicle = ManagingApp.VALID_VEHICLES[vehicle_type](brand, model, license_plate_number)
            self.vehicles.append(vehicle)
            return f"{brand} {model} was successfully uploaded with LPN-{license_plate_number}."

        return f"{license_plate_number} belongs to another vehicle."

    def allow_route(self, start_point: str, end_point: str, length: float):
        route_id = len(self.routes) + 1

        try:
            duplicate_route = [r for r in self.routes if r.start_point == start_point and
                               r.end_point == end_point and r.length == length][0]

        except IndexError:
            try:
                shorter_route = [r for r in self.routes if r.start_point == start_point and
                                 r.end_point == end_point and r.length < length][0]

            except IndexError:
                route = Route(start_point, end_point, length, route_id)
                self.routes.append(route)
                try:
                    route_to_lock = [r for r in self.routes if r.start_point == start_point and
                                     r.end_point == end_point and r.length > length][0]
                    route_to_lock.is_locked = True
                except IndexError:
                    pass
                return f"{start_point}/{end_point} - {length} km is unlocked and available to use."

            return f"{start_point}/{end_point} shorter route had already been added to our platform."

        return f"{start_point}/{end_point} - {length} km had already been added to our platform."

    def make_trip(self, driving_license_number: str, license_plate_number: str, route_id: int,
                  is_accident_happened: bool):
        user = next(filter(lambda u: u.driving_license_number == driving_license_number, self.users))
        vehicle = next(filter(lambda v: v.license_plate_number == license_plate_number, self.vehicles))
        route = next(filter(lambda r: r.route_id == route_id, self.routes))

        if user.is_blocked:
            return f"User {driving_license_number} is blocked in the platform! This trip is not allowed."

        if vehicle.is_damaged:
            return f"Vehicle {license_plate_number} is damaged! This trip is not allowed."

        if route.is_locked:
            return f"Route {route_id} is locked! This trip is not allowed."

        vehicle.drive(route.length)
        if is_accident_happened:
            vehicle.change_status()
            user.decrease_rating()
        else:
            user.increase_rating()

        return str(vehicle)

    def repair_vehicles(self, count: int):
        vehicles_to_repair = [v for v in self.vehicles if v.is_damaged]
        vehicles_to_repair = sorted(vehicles_to_repair, key=lambda x: (x.brand, x.model))

        for i in range(count):
            if i == len(vehicles_to_repair):
                break
            vehicles_to_repair[i].change_status()
            vehicles_to_repair[i].recharge()

        return f"{len(vehicles_to_repair)} vehicles were successfully repaired!"

    def users_report(self):
        result = ["*** E-Drive-Rent ***"]
        for user in sorted(self.users, key=lambda x: -x.rating):
            result.append(str(user))

        return "\n".join(result)
