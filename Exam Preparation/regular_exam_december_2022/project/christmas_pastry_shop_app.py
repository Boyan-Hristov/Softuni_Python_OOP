from typing import List
from project.booths.booth import Booth
from project.booths.open_booth import OpenBooth
from project.booths.private_booth import PrivateBooth
from project.delicacies.delicacy import Delicacy
from project.delicacies.gingerbread import Gingerbread
from project.delicacies.stolen import Stolen


class ChristmasPastryShopApp:
    VALID_DELICACIES = {"Gingerbread": Gingerbread, "Stolen": Stolen}
    VALID_BOOTHS = {"Open Booth": OpenBooth, "Private Booth": PrivateBooth}

    def __init__(self):
        self.booths: List[Booth] = []
        self.delicacies: List[Delicacy] = []
        self.income: float = 0.0

    def add_delicacy(self, type_delicacy: str, name: str, price: float):
        try:
            next(filter(lambda d: d.name == name, self.delicacies))
            raise Exception("{delicacy name} already exists!")
        except StopIteration:
            if type_delicacy not in self.VALID_DELICACIES.keys():
                raise Exception(f"{type_delicacy} is not on our delicacy menu!")

            delicacy = self.VALID_DELICACIES[type_delicacy](name, price)
            self.delicacies.append(delicacy)
            return f"Added delicacy {name} - {type_delicacy} to the pastry shop."

    def add_booth(self, type_booth: str, booth_number: int, capacity: int):
        try:
            next(filter(lambda b: b.booth_number == booth_number, self.booths))
            raise Exception(f"Booth number {booth_number} already exists!")
        except StopIteration:
            if type_booth not in self.VALID_BOOTHS.keys():
                raise Exception(f"{type_booth} is not a valid booth!")
            booth = self.VALID_BOOTHS[type_booth](booth_number, capacity)
            self.booths.append(booth)
            return f"Added booth number {booth_number} in the pastry shop."

    def reserve_booth(self, number_of_people: int):
        for booth in self.booths:
            if not booth.is_reserved and booth.capacity >= number_of_people:
                booth.reserve(number_of_people)
                return f"Booth {booth.booth_number} has been reserved for {number_of_people} people."
        else:
            raise Exception(f"No available booth for {number_of_people} people!")

    def order_delicacy(self, booth_number: int, delicacy_name: str):
        try:
            booth = next(filter(lambda b: b.booth_number == booth_number, self.booths))
        except StopIteration:
            raise Exception(f"Could not find booth {booth_number}!")

        try:
            delicacy = next(filter(lambda d: d.name == delicacy_name, self.delicacies))
        except StopIteration:
            raise Exception(f"No {delicacy_name} in the pastry shop!")

        booth.delicacy_orders.append(delicacy)
        return f"Booth {booth_number} ordered {delicacy_name}."

    def leave_booth(self, booth_number: int):
        booth = next(filter(lambda b: b.booth_number == booth_number, self.booths))
        booth_bill = booth.price_for_reservation + sum([d.price for d in booth.delicacy_orders])
        self.income += booth_bill
        booth.delicacy_orders.clear()
        booth.is_reserved = False
        booth.price_for_reservation = 0

        return f"Booth {booth_number}:\n" \
               f"Bill: {booth_bill:.2f}lv."

    def get_income(self):
        return f"Income: {self.income:.2f}lv."
