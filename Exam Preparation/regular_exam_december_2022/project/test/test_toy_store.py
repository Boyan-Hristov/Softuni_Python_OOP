from project.toy_store import ToyStore
from unittest import TestCase, main


class TestToyStore(TestCase):

    def setUp(self) -> None:
        self.store = ToyStore()

    def test_correct_init(self):
        self.assertIsNone(self.store.toy_shelf["A"])
        self.assertIsNone(self.store.toy_shelf["B"])
        self.assertIsNone(self.store.toy_shelf["C"])
        self.assertIsNone(self.store.toy_shelf["D"])
        self.assertIsNone(self.store.toy_shelf["E"])
        self.assertIsNone(self.store.toy_shelf["F"])
        self.assertIsNone(self.store.toy_shelf["G"])

    def test_add_toy_failure_invalid_shelf_raises_exception(self):
        with self.assertRaises(Exception) as ex:
            self.store.add_toy("K", "ball")
        self.assertEqual("Shelf doesn't exist!", str(ex.exception))

    def test_add_toy_failure_toy_already_added_raises_exception(self):
        self.store.toy_shelf["A"] = "ball"
        with self.assertRaises(Exception) as ex:
            self.store.add_toy("A", "ball")
        self.assertEqual("Toy is already in shelf!", str(ex.exception))

    def test_add_toy_failure_shelf_is_already_taken_raises_exception(self):
        self.store.toy_shelf["A"] = "ball"
        with self.assertRaises(Exception) as ex:
            self.store.add_toy("A", "car")
        self.assertEqual("Shelf is already taken!", str(ex.exception))

    def test_add_toy_success_toy_added_in_shelf(self):
        self.assertIsNone(self.store.toy_shelf["A"])
        result = self.store.add_toy("A", "ball")
        self.assertEqual("Toy:ball placed successfully!", result)
        self.assertEqual("ball", self.store.toy_shelf["A"])

    def test_remove_toy_failure_shelf_doesnt_exist_raises_exception(self):
        with self.assertRaises(Exception) as ex:
            self.store.remove_toy("K", "ball")
        self.assertEqual("Shelf doesn't exist!", str(ex.exception))

    def test_remove_toy_failure_toy_doesnt_exist_raises_exception(self):
        with self.assertRaises(Exception) as ex:
            self.store.remove_toy("A", "ball")
        self.assertEqual("Toy in that shelf doesn't exists!", str(ex.exception))

    def test_remove_toy_success_toy_removed_from_shelf(self):
        self.store.toy_shelf["A"] = "ball"
        result = self.store.remove_toy("A", "ball")
        self.assertEqual("Remove toy:ball successfully!", result)
        self.assertIsNone(self.store.toy_shelf["A"])


if __name__ == "__main__":
    main()