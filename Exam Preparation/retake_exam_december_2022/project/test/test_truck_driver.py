from project.truck_driver import TruckDriver
from unittest import TestCase, main


class TestTruckDriver(TestCase):

    def setUp(self) -> None:
        self.driver = TruckDriver("Ivan", 10)

    def test_correct_init(self):
        self.assertEqual("Ivan", self.driver.name)
        self.assertEqual(10.0, self.driver.money_per_mile)
        self.assertEqual({}, self.driver.available_cargos)
        self.assertEqual(0.0, self.driver.earned_money)
        self.assertEqual(0, self.driver.miles)

    def test_earned_money_setter_invalid_value_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.driver.earned_money = -0.1
        self.assertEqual(f"{self.driver.name} went bankrupt.",
                         str(ve.exception))

    def test_add_cargo_offer_failure_cargo_offer_already_added(self):
        self.driver.available_cargos = {"Sofia": 100}
        with self.assertRaises(Exception) as ex:
            self.driver.add_cargo_offer("Sofia", 150)
        self.assertEqual("Cargo offer is already added.", str(ex.exception))
        self.assertEqual(1, len(self.driver.available_cargos))

    def test_add_cargo_offer_success_cargo_added(self):
        self.assertEqual(0, len(self.driver.available_cargos))
        result = self.driver.add_cargo_offer("Sofia", 100)
        self.assertEqual("Cargo for 100 to "
                         "Sofia was added as an offer.",
                         result)
        self.assertEqual(1, len(self.driver.available_cargos))

    def test_drive_best_cargo_offer_failure_no_offers_raises_value_error(self):
        result = self.driver.drive_best_cargo_offer()
        self.assertEqual("There are no offers available.",
                         result)

    def test_drive_best_cargo_offer_success_adds_money_and_miles(self):
        self.driver.available_cargos = {"Sofia": 10_000, "Plovdiv": 20_000}
        result = self.driver.drive_best_cargo_offer()
        self.assertEqual(20_000, self.driver.miles)
        self.assertEqual(f"{self.driver.name} is driving 20000 to Plovdiv.",
                         result)
        self.assertEqual(176_000.0, self.driver.earned_money)

    def test_represent_expected_corresponding_string(self):
        self.driver.miles = 15_000
        self.assertEqual(f"Ivan has 15000 miles behind his back.",
                         str(self.driver))


if __name__ == "__main__":
    main()
