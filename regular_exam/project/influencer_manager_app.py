from project.campaigns.high_budget_campaign import HighBudgetCampaign
from project.campaigns.low_budget_campaign import LowBudgetCampaign
from project.influencers.premium_influencer import PremiumInfluencer
from project.influencers.standard_influencer import StandardInfluencer


class InfluencerManagerApp:
    VALID_INFLUENCERS = {"PremiumInfluencer": PremiumInfluencer,
                         "StandardInfluencer": StandardInfluencer}
    VALID_CAMPAIGNS = {"HighBudgetCampaign": HighBudgetCampaign,
                       "LowBudgetCampaign": LowBudgetCampaign}

    def __init__(self):
        self.influencers = []
        self.campaigns = []

    def register_influencer(self, influencer_type: str, username: str, followers: int, engagement_rate: float):
        if influencer_type not in self.VALID_INFLUENCERS.keys():
            return f"{influencer_type} is not an allowed influencer type."

        try:
            next(filter(lambda i: i.username == username, self.influencers))
            return f"{username} is already registered."
        except StopIteration:
            influencer = self.VALID_INFLUENCERS[influencer_type](username, followers, engagement_rate)
            self.influencers.append(influencer)
            return f"{username} is successfully registered as a {influencer_type}."

    def create_campaign(self, campaign_type: str, campaign_id: int, brand: str, required_engagement: float):
        if campaign_type not in self.VALID_CAMPAIGNS.keys():
            return f"{campaign_type} is not a valid campaign type."

        try:
            next(filter(lambda c: c.campaign_id == campaign_id, self.campaigns))
            return f"Campaign ID {campaign_id} has already been created."
        except StopIteration:
            campaign = self.VALID_CAMPAIGNS[campaign_type](campaign_id, brand, required_engagement)
            self.campaigns.append(campaign)
            return f"Campaign ID {campaign_id} for {brand} is successfully created as a {campaign_type}."

    def participate_in_campaign(self, influencer_username: str, campaign_id: int):
        try:
            influencer = next(filter(lambda i: i.username == influencer_username, self.influencers))
        except StopIteration:
            return f"Influencer '{influencer_username}' not found."

        try:
            campaign = next(filter(lambda c: c.campaign_id == campaign_id, self.campaigns))
        except StopIteration:
            return f"Campaign with ID {campaign_id} not found."

        if not campaign.check_eligibility(influencer.engagement_rate):
            return f"Influencer '{influencer_username}' does not meet " \
                   f"the eligibility criteria for the campaign with ID {campaign_id}."

        payment = influencer.calculate_payment(campaign)
        if payment > 0:
            campaign.approved_influencers.append(influencer)
            campaign.budget -= payment
            influencer.campaigns_participated.append(campaign)
            return f"Influencer '{influencer_username}' has successfully " \
                   f"participated in the campaign with ID {campaign_id}."

        return

    def calculate_total_reached_followers(self):
        result = {}
        for campaign in self.campaigns:
            if not campaign.approved_influencers:
                continue
            total_followers = 0
            for influencer in campaign.approved_influencers:
                total_followers += influencer.reached_followers(campaign.__class__.__name__)
            result[campaign] = total_followers

        return result

    def influencer_campaign_report(self, username: str):
        influencer = next(filter(lambda i: i.username == username, self.influencers))
        return influencer.display_campaigns_participated()

    def campaign_statistics(self):
        result = ["$$ Campaign Statistics $$"]
        for campaign in sorted(self.campaigns, key=lambda c: (len(c.approved_influencers), -c.budget)):
            if campaign.approved_influencers:
                result.append(f"  * Brand: {campaign.brand}, "
                              f"Total influencers: {len(campaign.approved_influencers)}, "
                              f"Total budget: ${campaign.budget:.2f}, "
                              f"Total reached followers: {campaign.reached_followers()}")

        return "\n".join(result)
