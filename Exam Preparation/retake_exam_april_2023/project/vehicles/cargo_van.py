from project.vehicles.base_vehicle import BaseVehicle


class CargoVan(BaseVehicle):
    MAX_MILEAGE = 180
    LOAD_BATTERY_REDUCER = 5

    def __init__(self, brand: str, model: str, license_plate_number: str):
        super().__init__(brand, model, license_plate_number, self.MAX_MILEAGE)

    def drive(self, mileage: float):
        # doesn't work for some reason
        # battery_used = round(mileage / self.MAX_MILEAGE * 100) + self.LOAD_BATTERY_REDUCER
        # self.battery_level -= battery_used
        self.battery_level -= (round(mileage / self.MAX_MILEAGE * 100) + self.LOAD_BATTERY_REDUCER)
