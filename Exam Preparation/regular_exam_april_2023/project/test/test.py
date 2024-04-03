from project.tennis_player import TennisPlayer
from unittest import TestCase, main


class TestTennisPlayer(TestCase):

    def setUp(self) -> None:
        self.player = TennisPlayer("Grisho", 30, 150)

    def test_correct_init(self):
        self.assertEqual("Grisho", self.player.name)
        self.assertEqual(30, self.player.age)
        self.assertEqual(150, self.player.points)
        self.assertEqual([], self.player.wins)

    def test_name_setter_invalid_value_two_chars_expected_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.player.name = "Ab"
        self.assertEqual("Name should be more than 2 symbols!",
                         str(ve.exception))

    def test_name_setter_invalid_value_one_char_expected_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.player.name = "A"
        self.assertEqual("Name should be more than 2 symbols!",
                         str(ve.exception))

    def test_age_setter_invalid_value_expected_raises_value_error(self):
        with self.assertRaises(ValueError) as ve:
            self.player.age = 15
        self.assertEqual("Players must be at least 18 years of age!",
                         str(ve.exception))

    def test_add_new_win_failure_expected_no_change(self):
        self.player.wins = ["Australia Open"]
        tournament_name = "Australia Open"
        result = self.player.add_new_win(tournament_name)
        self.assertEqual(1, len(self.player.wins))
        self.assertEqual(f"{tournament_name} has been already added to the list of wins!",
                         result)

    def test_add_new_win_expected_tournament_added_to_wins(self):
        self.assertEqual(0, len(self.player.wins))
        self.player.add_new_win("Wimbledon")
        self.assertEqual(1, len(self.player.wins))

    def test_less_than_smaller_value_expected_corresponding_string(self):
        other = TennisPlayer("Djokovic", 33, 200)
        result = self.player < other
        self.assertEqual(f'{other.name} is a top seeded player '
                         f'and he/she is better than {self.player.name}',
                         result)

    def test_less_than_equal_value_expected_corresponding_string(self):
        other = TennisPlayer("Djokovic", 33, 150)
        result = self.player < other
        self.assertEqual(f'{self.player.name} is a better player than {other.name}',
                         result)

    def test_less_than_greater_value_expected_corresponding_string(self):
        other = TennisPlayer("Djokovic", 33, 100)
        result = self.player < other
        self.assertEqual(f'{self.player.name} is a better player than {other.name}',
                         result)

    def test_string_representation_expected_corresponding_string(self):
        self.player.add_new_win("Wimbledon")
        self.player.add_new_win("Australia Open")
        expected_result = "Tennis Player: Grisho\n" \
                          "Age: 30\n" \
                          "Points: 150.0\n" \
                          "Tournaments won: Wimbledon, Australia Open"
        result = str(self.player)
        self.assertEqual(expected_result, result)


if __name__ == "__main__":
    main()
