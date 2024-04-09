from project.campaigns.base_campaign import BaseCampaign
from project.influencers.base_influencer import BaseInfluencer


class PremiumInfluencer(BaseInfluencer):
    INITIAL_PAYMENT_PERCENTAGE = 0.85
    CAMPAIGN_MULTIPLIER = {"LowBudgetCampaign": 0.8,
                           "HighBudgetCampaign": 1.5}

    def calculate_payment(self, campaign: BaseCampaign):
        payment = campaign.budget * self.INITIAL_PAYMENT_PERCENTAGE
        return float(payment)

    def reached_followers(self, campaign_type: str):
        multiplier = self.CAMPAIGN_MULTIPLIER[campaign_type]
        reached_followers = self.followers * self.engagement_rate * multiplier
        return int(reached_followers)
