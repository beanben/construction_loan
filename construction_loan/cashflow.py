import pandas as pd
from construction_loan.utils import time_execution, dataframe_to_csv

class Cashflow:
    billing_period = 'end of calendar month'

    def __init__(self, data):
            if isinstance(data, pd.DataFrame):
                self.df = data
            else:
                raise ValueError("Invalid input type for CashFlow initialization: the input must be a DataFrame")
    
    @classmethod
    @time_execution
    def from_budget(cls, budget_instance):

        # get the budget dataframe
        budget_df = budget_instance.df

        # Calculate the number of days and daily cost
        budget_df['num_days'] = (pd.to_datetime(budget_df['end_date']) - pd.to_datetime(budget_df['start_date'])).dt.days + 1
        budget_df['daily_cost'] = (budget_df['amount'] / budget_df['num_days']).round(2)

        # Define columns index
        index_col = pd.MultiIndex.from_frame(budget_df[["cost_category", "cost_type", "supplier"]])

        # Define time index
        start_date = budget_df['start_date'].min()
        end_date = budget_df['end_date'].max()
        index = pd.date_range(start_date, end_date, freq='D', name='date')

        # Initialize cashflow DataFrame
        cashflow_df = pd.DataFrame(index=index, columns=index_col).fillna(0.0).astype(float)

        # Spread costs
        for _, row in budget_df.iterrows():
            daily_costs = pd.Series([row['daily_cost']] * row['num_days'], 
                                    index=pd.date_range(row['start_date'], periods=row['num_days'], freq='D'))
            
            # amend the last days' cost with the difference between the total cost and the sum of the daily costs, to ensure rouding errors are accounted for
            daily_costs.iloc[-1] += row['amount'] - daily_costs.sum()
            cashflow_df.loc[daily_costs.index, (row['cost_category'], row['cost_type'], row['supplier'])] += daily_costs.values

        return cls(cashflow_df)

    # @classmethod
    # def from_csv(cls, csv_file_path):
    #     # Logic to read cash flow data directly from CSV
    #     cashflow_df = ...  # Read and process CSV file to create cash flow DataFrame
    #     return cls(cashflow_df)

    def total_cost(self):
        return self.df.sum().sum()
    
    def costs_grouped_by_billing_period(self):
        billing_period = 'M' if self.billing_period == 'end of calendar month' else 'D'
        return self.df.resample(billing_period).sum()
    
    def costs_grouped_by_level(self, level):
        return self.df.sum(level=level, axis=1)
    
    def df_to_csv(self, csv_file_path):
        dataframe_to_csv(self.df, csv_file_path)
    
