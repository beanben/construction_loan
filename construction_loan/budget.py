# import pandas as pd
# from construction_loan.utils import (read_csv_to_dataframe, 
#                     validate_columns, 
#                     validate_amount_column, 
#                     validate_date_format_columns,
#                     validate_start_date_before_end_date,
#                     fill_empty_values_of_string_columns,
#                     time_execution)
                   

# class Budget:
#     def __init__(self, data):
#             if isinstance(data, pd.DataFrame):
#                 self.df = data
#             else:
#                 raise ValueError("Invalid input type for Budget initialization: the input must be a DataFrame")
    
#     @classmethod
#     # @time_execution
#     def from_csv(cls, csv_file_path: str) -> pd.DataFrame:
#         # Read the CSV file into a DataFrame
#         budget_df = read_csv_to_dataframe(csv_file_path)

#         # Define the required columns
#         required_columns = ['cost_category', 'cost_type', 'supplier', 'amount', 'start_date', 'end_date']

#         # fill in the emptuy values of cost_category, cost_type and supplier with 'NoData'
#         budget_df[['cost_category', 'cost_type', 'supplier']] = budget_df[['cost_category', 'cost_type', 'supplier']].astype(str)
#         fill_empty_values_of_string_columns(budget_df, ['cost_category', 'cost_type', 'supplier'])

#         # Perform validations
#         validate_columns(budget_df, required_columns)
#         validate_amount_column(budget_df, 'amount')
#         validate_date_format_columns(budget_df, ['start_date', 'end_date'])
#         validate_start_date_before_end_date(budget_df, 'start_date', 'end_date')
#         # validate_cost_category_not_empty(budget_df, 'cost_category')

#         return cls(budget_df)
    
#     def total_cost(self):
#         return self.df.amount.sum()
    
#     def costs_grouped_by_level(self, category):
#         df = self.df.groupby(by=category, sort=False).amount.sum()

#         # add a total row
#         df.loc['Total'] = df.sum()
#         return df

class Budget:
    def __init__(self, project_costs, loan_amount, interest, equity):
        self.project_costs = project_costs
        self.loan_amount = loan_amount
        self.interest = interest
        self.equity = equity

    def total_funding_needed(self):
        return self.project_costs.total_costs() + self.interest

    def funding_sources(self):
        return {'Loan': self.loan_amount, 'Equity': self.equity}

# class ProjectCosts:
#     def __init__(self, material_costs, labor_costs, other_costs):
#         self.material_costs = material_costs
#         self.labor_costs = labor_costs
#         self.other_costs = other_costs

#     def total_costs(self):
#         return self.material_costs + self.labor_costs + self.other_costs


# class LoanAppraisal:
#     def __init__(self, project_costs, funding_percentage, loan_rate, duration):
#         self.project_costs = project_costs
#         self.funding_percentage = funding_percentage
#         self.loan_rate = loan_rate
#         self.duration = duration

#     def calculate_loan_offer(self):
#         loan_amount = self.project_costs.total_costs() * self.funding_percentage / 100
#         interest = loan_amount * self.loan_rate * self.duration
#         return loan_amount, interest


# class Budget:
#     def __init__(self, project_costs, loan_amount, interest, equity):
#         self.project_costs = project_costs
#         self.loan_amount = loan_amount
#         self.interest = interest
#         self.equity = equity

#     def total_funding_needed(self):
#         return self.project_costs.total_costs() + self.interest

#     def funding_sources(self):
#         return {'Loan': self.loan_amount, 'Equity': self.equity}


# # Example usage
# project_costs = ProjectCosts(material_costs=50000, labor_costs=30000, other_costs=20000)
# loan_appraisal = LoanAppraisal(project_costs, funding_percentage=70, loan_rate=0.05, duration=5)
# loan_amount, interest = loan_appraisal.calculate_loan_offer()
# budget = Budget(project_costs, loan_amount, interest, equity=project_costs.total_costs() - loan_amount)

# print("Total Funding Needed:", budget.total_funding_needed())
# print("Funding Sources:", budget.funding_sources())
