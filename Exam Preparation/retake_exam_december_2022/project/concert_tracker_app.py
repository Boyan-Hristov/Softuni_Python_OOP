from typing import List
from project.band import Band
from project.band_members.drummer import Drummer
from project.band_members.guitarist import Guitarist
from project.band_members.musician import Musician
from project.band_members.singer import Singer
from project.concert import Concert


class ConcertTrackerApp:
    VALID_MUSICIANS = {
        "Guitarist": Guitarist,
        "Drummer": Drummer,
        "Singer": Singer
    }

    def __init__(self):
        self.bands: List[Band] = []
        self.musicians: List[Musician] = []
        self.concerts: List[Concert] = []

    def create_musician(self, musician_type: str, name: str, age: int):
        if musician_type not in self.VALID_MUSICIANS.keys():
            raise ValueError("Invalid musician type!")
        try:
            next(filter(lambda m: m.name == name, self.musicians))
            raise Exception(f"{name} is already a musician!")
        except StopIteration:
            musician = self.VALID_MUSICIANS[musician_type](name, age)
            self.musicians.append(musician)
            return f"{name} is now a {musician_type}."

    def create_band(self, name: str):
        try:
            next(filter(lambda b: b.name == name, self.bands))
            raise Exception(f"{name} band is already created!")
        except StopIteration:
            band = Band(name)
            self.bands.append(band)
            return f"{name} was created."

    def create_concert(self, genre: str, audience: int, ticket_price: float, expenses: float, place: str):
        try:
            duplicate = next(filter(lambda c: c.place == place, self.concerts))
            raise Exception(f"{place} is already registered for {duplicate.genre} concert!")
        except StopIteration:
            concert = Concert(genre, audience, ticket_price, expenses, place)
            self.concerts.append(concert)
            return f"{concert.genre} concert in {place} was added."

    def add_musician_to_band(self, musician_name: str, band_name: str):
        try:
            musician = next(filter(lambda m: m.name == musician_name, self.musicians))
        except StopIteration:
            raise Exception(f"{musician_name} isn't a musician!")

        try:
            band = next(filter(lambda b: b.name == band_name, self.bands))
        except StopIteration:
            raise Exception(f"{band_name} isn't a band!")

        # check if the musician should be removed from self.musicians
        # self.musicians.remove(musician)
        band.members.append(musician)
        return f"{musician_name} was added to {band_name}."

    def remove_musician_from_band(self, musician_name: str, band_name: str):
        try:
            band = next(filter(lambda b: b.name == band_name, self.bands))
        except StopIteration:
            raise Exception(f"{band_name} isn't a band!")

        try:
            musician = next(filter(lambda m: m.name == musician_name, band.members))
        except StopIteration:
            raise Exception(f"{musician_name} isn't a member of {band_name}!")

        # check if the musician should be added back to self.musicians
        # self.musicians.append(musician)
        band.members.remove(musician)
        return f"{musician_name} was removed from {band_name}."

    def start_concert(self, concert_place: str, band_name: str):
        band = next(filter(lambda b: b.name == band_name, self.bands))
        concert = next(filter(lambda c: c.place == concert_place, self.concerts))

        # check if logic works
        band_musicians = {m.__class__.__name__ for m in band.members}
        if len(band_musicians.intersection(self.VALID_MUSICIANS.keys())) < 3:
            raise Exception(f"{band_name} can't start the concert because it doesn't have enough members!")

        # check if list format is correct
        band_skills = [", ".join(m.skills) for m in band.members]
        needed_skills = concert.VALID_GENRES[concert.genre]

        for skill in needed_skills:
            if skill not in band_skills:
                raise Exception(f"The {band_name} band is not ready to play at the concert!")

        profit = concert.audience * concert.ticket_price - concert.expenses
        return f"{band_name} gained {profit:.2f}$ from the {concert.genre} concert in {concert_place}."
