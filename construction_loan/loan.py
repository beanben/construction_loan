import pandas as pd


class Loan:
    def __init__(self):
        self.total_commitment = None
        self.capital_commitment = None
        self.LTC_covenant = None
        self.LTV_covenant = None
        self.duration_months = None
        self.arrangement_fee_pct = None
        self.margin_pct = None
        self.non_utilisation_fee_pct = None
        self.exit_fee_pct = None
        self.fundable_costs = None

    def calculate_terms(self, fundable_costs, ltc_covenant, returns_targetted):
        # Set the fundable_costs, LTC_covenant, and returns_targetted
        self.fundable_costs = fundable_costs
        self.LTC_covenant = ltc_covenant
        
        # calculate minimum duration in months
        self.calculate_duration_months()

        # CONTINUE HERE

    def calculate_duration_months(self):
        # Assuming 'fundable_costs' has a DateTimeIndex
        if not self.fundable_costs.empty and isinstance(self.fundable_costs.index, pd.DatetimeIndex):
            start_date = self.fundable_costs.index.min()
            end_date = self.fundable_costs.index.max()

            # Calculate the difference in months
            duration = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

            # Assign duration to the class attribute
            self.duration_months = duration
        else:
            raise ValueError("Fundable costs are empty or do not have a DateTimeIndex.")
