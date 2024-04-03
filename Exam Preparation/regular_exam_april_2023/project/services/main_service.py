from project.services.base_service import BaseService


class MainService(BaseService):
    CAPACITY = 30
    VALID_ROBOTS = ["MaleRobot"]

    def __init__(self, name: str):
        super().__init__(name, capacity=self.CAPACITY)

    def details(self):
        result = f"{self.name} Main Service:\n"
        if not self.robots:
            result += "Robots: none"
        else:
            result += f"Robots: {' '.join([r.name for r in self.robots])}"

        return result
