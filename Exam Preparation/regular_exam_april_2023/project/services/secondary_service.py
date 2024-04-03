from project.services.base_service import BaseService


class SecondaryService(BaseService):
    CAPACITY = 15
    VALID_ROBOTS = ["FemaleRobot"]

    def __init__(self, name: str):
        super().__init__(name, capacity=self.CAPACITY)

    def details(self):
        result = f"{self.name} Secondary Service:\n"
        if not self.robots:
            result += "Robots: none"
        else:
            result += f"Robots: {' '.join([r.name for r in self.robots])}"

        return result
