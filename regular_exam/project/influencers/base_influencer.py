from abc import ABC, abstractmethod


class BaseInfluencer(ABC):
    # check if it should be 0.0 and 5.0
    MIN_ENGAGEMENT_RATE = 0
    MAX_ENGAGEMENT_RATE = 5

    def __init__(self, username: str, followers: int, engagement_rate: float):
        self.username = username
        self.followers = followers
        self.engagement_rate = engagement_rate
        self.campaigns_participated = []

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if not value.strip():
            raise ValueError("Username cannot be empty or consist only of whitespace!")
        self.__username = value

    @property
    def followers(self):
        return self.__followers

    @followers.setter
    def followers(self, value):
        if value < 0:
            raise ValueError("Followers must be a non-negative integer!")
        self.__followers = value

    @property
    def engagement_rate(self):
        return self.__engagement_rate

    @engagement_rate.setter
    def engagement_rate(self, value):
        # check
        if value < self.MIN_ENGAGEMENT_RATE or value > self.MAX_ENGAGEMENT_RATE:
            raise ValueError("Engagement rate should be between 0 and 5.")
        self.__engagement_rate = value

    @abstractmethod
    def calculate_payment(self, campaign):
        pass

    @abstractmethod
    def reached_followers(self, campaign_type: str):
        pass

    def display_campaigns_participated(self):
        if not self.campaigns_participated:
            return f"{self.username} has not participated in any campaigns."
        # check reached followers
        message = [f"{self.__class__.__name__} :) {self.username} :) participated in the following campaigns:"]
        for campaign in self.campaigns_participated:
            message.append(f"  - Campaign ID: {campaign.campaign_id}, "
                           f"Brand: {campaign.brand}, "
                           f"Reached followers: {self.reached_followers(campaign.__class__.__name__)}")

        return "\n".join(message)
