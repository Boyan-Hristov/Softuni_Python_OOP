from project.bookstore import Bookstore
from unittest import TestCase, main


class TestBookstore(TestCase):

    def setUp(self) -> None:
        self.bookstore = Bookstore(50)

    def test_correct_init(self):
        self.assertEqual(50, self.bookstore.books_limit)
        self.assertEqual({}, self.bookstore.availability_in_store_by_book_titles)
        self.assertEqual(0, self.bookstore.total_sold_books)

    def test_books_limit_setter_zero_value_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.bookstore.books_limit = 0
        self.assertEqual("Books limit of 0 is not valid", str(ve.exception))

    def test_books_limit_setter_less_than_zero_value_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.bookstore.books_limit = -5
        self.assertEqual("Books limit of -5 is not valid", str(ve.exception))

    def test_len(self):
        self.bookstore.availability_in_store_by_book_titles = {
            "book1": 20, "book2": 13, "book3": 7, "book4": 2, "book5": 0
        }
        self.assertEqual(42, len(self.bookstore))

    def test_receive_book_too_many_copies_raises_exception(self):
        self.bookstore.availability_in_store_by_book_titles = {"book1": 45}
        with self.assertRaises(Exception) as ex:
            self.bookstore.receive_book("book2", 6)
        self.assertEqual("Books limit is reached. Cannot receive more books!",
                         str(ex.exception))

    def test_receive_book_success_book_added(self):
        self.bookstore.availability_in_store_by_book_titles = {"book1": 15, "book2": 5}
        result = self.bookstore.receive_book("book2", 10)
        self.assertEqual("15 copies of book2 "
                         f"are available in the bookstore.",
                         result)
        self.assertEqual({"book1": 15, "book2": 15},
                         self.bookstore.availability_in_store_by_book_titles)

    def test_sell_book_failure_book_non_existent_raises_exception(self):
        with self.assertRaises(Exception) as ex:
            self.bookstore.sell_book("book1", 1)
        self.assertEqual("Book book1 doesn't exist!", str(ex.exception))

    def test_sell_book_failure_not_enough_books_raises_exception(self):
        self.bookstore.availability_in_store_by_book_titles = {"book1": 15, "book2": 5}
        with self.assertRaises(Exception) as ex:
            self.bookstore.sell_book("book2", 7)
        self.assertEqual("book2 has not enough copies to sell. Left: 5",
                         str(ex.exception))

    def test_sell_book_success_copies_reduced(self):
        self.bookstore.availability_in_store_by_book_titles = {"book1": 15, "book2": 5}
        result = self.bookstore.sell_book("book1", 5)
        self.assertEqual("Sold 5 copies of book1", result)
        self.assertEqual(10, self.bookstore.availability_in_store_by_book_titles["book1"])
        self.assertEqual(5, self.bookstore.total_sold_books)

    def test_str(self):
        self.bookstore.availability_in_store_by_book_titles = {"book1": 15, "book2": 5}
        self.bookstore.sell_book("book1", 5)
        self.bookstore.sell_book("book2", 3)
        expected = "Total sold books: 8\n" \
                   "Current availability: 12\n" \
                   " - book1: 10 copies\n" \
                   " - book2: 2 copies"
        self.assertEqual(expected, str(self.bookstore))


if __name__ == "__main__":
    main()
