from unittest import TestCase, main
from project.robot import Robot


class TestRobot(TestCase):

    def setUp(self) -> None:
        self.robot = Robot("1234", "Military", 1024, 1000)

    def test_correct_init(self):
        self.assertEqual("1234", self.robot.robot_id)
        self.assertEqual("Military", self.robot.category)
        self.assertEqual(1024, self.robot.available_capacity)
        self.assertEqual(1000, self.robot.price)
        self.assertEqual([], self.robot.hardware_upgrades)
        self.assertEqual([], self.robot.software_updates)

    def test_category_setter_invalid_category_expected_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.robot.category = "category"
        self.assertEqual(f"Category should be one of '{self.robot.ALLOWED_CATEGORIES}'",
                         str(ve.exception))

    def test_price_setter_invalid_price_expected_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.robot.price = -1
        self.assertEqual("Price cannot be negative!", str(ve.exception))

    def test_upgrade_failure_component_already_upgraded_expected_no_upgrade(self):
        self.robot.hardware_upgrades = ["night vision"]
        result = self.robot.upgrade("night vision", 200)
        self.assertEqual(f"Robot {self.robot.robot_id} was not upgraded.",
                         result)

    def test_upgrade_success_expected_component_added_price_increased(self):
        result = self.robot.upgrade("night vision", 200)
        self.assertEqual(["night vision"], self.robot.hardware_upgrades)
        self.assertEqual(1300, self.robot.price)
        self.assertEqual(f'Robot {self.robot.robot_id} was upgraded with night vision.',
                         result)

    def test_update_failure_older_version_expected_no_update(self):
        self.robot.software_updates = [2.0]
        result = self.robot.update(1.5, 512)
        self.assertEqual(f"Robot {self.robot.robot_id} was not updated.",
                         result)

    def test_update_failure_not_enough_capacity_expected_no_update(self):
        self.robot.software_updates = [1.0]
        result = self.robot.update(2.0, 2048)
        self.assertEqual(f"Robot {self.robot.robot_id} was not updated.",
                         result)

    def test_update_success_expected_software_added_capacity_decreased(self):
        result = self.robot.update(1.0, 512)
        self.assertEqual([1.0], self.robot.software_updates)
        self.assertEqual(512, self.robot.available_capacity)
        self.assertEqual(f'Robot {self.robot.robot_id} was updated to version 1.0.',
                         result)

    def test_gt_higher_price(self):
        new_robot = Robot("4321", "Education", 1024, 500)
        result = self.robot > new_robot
        self.assertEqual(f'Robot with ID {self.robot.robot_id} is more expensive '
                         f'than Robot with ID {new_robot.robot_id}.',
                         result)

    def test_gt_equal_price(self):
        new_robot = Robot("4321", "Education", 1024, 1000)
        result = self.robot > new_robot
        self.assertEqual(f'Robot with ID {self.robot.robot_id} costs equal to '
                         f'Robot with ID {new_robot.robot_id}.',
                         result)

    def test_gt_lower_price(self):
        new_robot = Robot("4321", "Education", 1024, 1500)
        result = self.robot > new_robot
        self.assertEqual(f'Robot with ID {self.robot.robot_id} is cheaper than '
                         f'Robot with ID {new_robot.robot_id}.',
                         result)


if __name__ == "__main__":
    main()
