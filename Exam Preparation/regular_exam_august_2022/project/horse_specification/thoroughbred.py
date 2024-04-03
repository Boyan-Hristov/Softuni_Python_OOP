from project.horse_specification.horse import Horse


class Thoroughbred(Horse):
    MAX_SPEED = 140

    def train(self):
        self.speed = min(self.speed + 3, self.MAX_SPEED)
