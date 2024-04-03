from typing import List

from project.horse_race import HorseRace
from project.horse_specification.appaloosa import Appaloosa
from project.horse_specification.horse import Horse
from project.horse_specification.thoroughbred import Thoroughbred
from project.jockey import Jockey


class HorseRaceApp:
    VALID_HORSES = {"Appaloosa": Appaloosa, "Thoroughbred": Thoroughbred}

    def __init__(self):
        self.horses: List[Horse] = []
        self.jockeys: List[Jockey] = []
        self.horse_races: List[HorseRace] = []
        self.races_count = {"Winter": 0,
                      "Spring": 0,
                      "Autumn": 0,
                      "Summer": 0}

    def add_horse(self, horse_type: str, horse_name: str, horse_speed: int):
        if horse_type not in self.VALID_HORSES.keys():
            raise Exception("Horse {horse_name} has been already added!")

        try:
            next(filter(lambda h: h.name == horse_name, self.horses))
            raise Exception(f"Horse {horse_name} has been already added!")

        except StopIteration:
            horse = self.VALID_HORSES[horse_type](horse_name, horse_speed)
            self.horses.append(horse)
            return f"{horse_type} horse {horse_name} is added."

    def add_jockey(self, jockey_name, age: int):
        try:
            next(filter(lambda j: j.name == jockey_name, self.jockeys))
            raise Exception(f"Jockey {jockey_name} has been already added!")
        except StopIteration:
            jockey = Jockey(jockey_name, age)
            self.jockeys.append(jockey)
            return f"Jockey {jockey_name} is added."

    def create_horse_race(self, race_type: str):
        if self.races_count[race_type] == 1:
            raise Exception(f"Race {race_type} has been already created!")
        self.races_count[race_type] += 1
        horse_race = HorseRace(race_type)
        self.horse_races.append(horse_race)
        return f"Race {race_type} is created."

    def add_horse_to_jockey(self, jockey_name: str, horse_type: str):
        try:
            jockey = next(filter(lambda j: j.name == jockey_name, self.jockeys))
        except StopIteration:
            raise Exception(f"Jockey {jockey_name} could not be found!")

        try:
            horse = [h for h in self.horses if h.__class__.__name__ == horse_type and not h.is_taken][-1]
        except IndexError:
            raise Exception(f"Horse breed {horse_type} could not be found!")

        if jockey.horse is not None:
            return f"Jockey {jockey_name} already has a horse."

        jockey.horse = horse
        horse.is_taken = True
        return f"Jockey {jockey_name} will ride the horse {horse.name}."

    def add_jockey_to_horse_race(self, race_type: str, jockey_name: str):
        try:
            race = next(filter(lambda r: r.race_type == race_type, self.horse_races))
        except StopIteration:
            raise Exception(f"Race {race_type} could not be found!")

        try:
            jockey = next(filter(lambda j: j.name == jockey_name, self.jockeys))
        except StopIteration:
            raise Exception(f"Jockey {jockey_name} could not be found!")

        if jockey.horse is None:
            raise Exception(f"Jockey {jockey_name} cannot race without a horse!")

        if jockey in race.jockeys:
            return f"Jockey {jockey_name} has been already added to the {race_type} race."

        race.jockeys.append(jockey)
        return f"Jockey {jockey_name} added to the {race_type} race."

    def start_horse_race(self, race_type: str):
        try:
            race = next(filter(lambda r: r.race_type == race_type, self.horse_races))
        except StopIteration:
            raise Exception(f"Race {race_type} could not be found!")

        if len(race.jockeys) < 2:
            raise Exception(f"Horse race {race_type} needs at least two participants!")

        winner = max(race.jockeys, key=lambda j: j.horse.speed)

        return f"The winner of the {race_type} race, " \
               f"with a speed of {winner.horse.speed}km/h " \
               f"is {winner.name}! Winner's horse: {winner.horse.name}."
