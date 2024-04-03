from typing import List
from project.robots.base_robot import BaseRobot
from project.robots.female_robot import FemaleRobot
from project.robots.male_robot import MaleRobot
from project.services.base_service import BaseService
from project.services.main_service import MainService
from project.services.secondary_service import SecondaryService


class RobotsManagingApp:
    VALID_SERVICES = {"MainService": MainService, "SecondaryService": SecondaryService}
    VALID_ROBOTS = {"MaleRobot": MaleRobot, "FemaleRobot": FemaleRobot}

    def __init__(self):
        self.robots: List[BaseRobot] = []
        self.services: List[BaseService] = []

    def add_service(self, service_type: str, name: str):
        try:
            service = self.VALID_SERVICES[service_type](name)
            self.services.append(service)
            return f"{service_type} is successfully added."

        except KeyError:
            raise Exception("Invalid service type!")

    def add_robot(self, robot_type: str, name: str, kind: str, price: float):
        try:
            robot = self.VALID_ROBOTS[robot_type](name, kind, price)
            self.robots.append(robot)
            return f"{robot_type} is successfully added."

        except KeyError:
            raise Exception("Invalid robot type!")

    def add_robot_to_service(self, robot_name: str, service_name: str):
        robot = next(filter(lambda r: r.name == robot_name, self.robots))
        service = next(filter(lambda s: s.name == service_name, self.services))

        if robot.__class__.__name__ not in service.VALID_ROBOTS:
            return "Unsuitable service."

        if service.capacity < len(service.robots):
            raise Exception("Not enough capacity for this robot!")

        self.robots.remove(robot)
        service.robots.append(robot)
        return f"Successfully added {robot_name} to {service_name}."

    def remove_robot_from_service(self, robot_name: str, service_name: str):
        service = next(filter(lambda s: s.name == service_name, self.services))
        try:
            robot = next(filter(lambda r: r.name == robot_name, service.robots))
            service.robots.remove(robot)
            self.robots.append(robot)
            return f"Successfully removed {robot_name} from {service_name}."

        except StopIteration:
            raise Exception("No such robot in this service!")

    def feed_all_robots_from_service(self, service_name: str):
        service = next(filter(lambda s: s.name == service_name, self.services))
        for robot in service.robots:
            robot.eating()

        return f"Robots fed: {len(service.robots)}."

    def service_price(self, service_name: str):
        service = next(filter(lambda s: s.name == service_name, self.services))
        total_price = sum([r.price for r in service.robots])
        return f"The value of service {service_name} is {total_price:.2f}."

    def __str__(self):
        result = ""
        result += "\n".join([s.details() for s in self.services])
        return result
