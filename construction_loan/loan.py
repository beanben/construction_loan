import pandas as pd


class Loan:
    def __init__(
            self,
            total_commitment,
            capital_commitment,
            LTC_covenant, 
            LTV_covenant, 
            duration_months, 
            arrangement_fee_pct, 
            margin_pct, 
            non_utilisation_fee_pct, 
            exit_fee_pct):

        self.total_commitment = total_commitment
        self.capital_commitment = capital_commitment
        self.LTC_covenant = LTC_covenant
        self.LTV_covenant = LTV_covenant
        self.duration_months = duration_months
        self.arrangement_fee_pct = arrangement_fee_pct
        self.margin_pct = margin_pct
        self.non_utilisation_fee_pct = non_utilisation_fee_pct
        self.exit_fee_pct = exit_fee_pct

    

    # @classmethod
    # def size_from_budget(cls, budget, **kwargs):
    #     """
    #     Class method to create a Loan instance from a budget.

    #     :param budget: Total budget or cost of the project being funded.
    #     """
    #     loan_instance = cls(**kwargs)

    #     # Additional logic for budget-based loan sizing
    #     return loan_instance

    # def set_terms(self, **kwargs):
    #     """
    #     Method to set the terms of the loan.

    #     :param kwargs: Additional terms of the loan.
    #     """
    #     for key, value in kwargs.items():
    #         if hasattr(self, key):
    #             setattr(self, key, value)
    #         else:
    #             print(f"Attribute '{key}' does not exist in the Loan class.")
