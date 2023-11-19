import pandas as pd
from budget import Budget

class CashFlow:
    def __init__(self, data):
            if isinstance(data, pd.DataFrame):
                self.df = data
            else:
                raise ValueError("Invalid input type for CashFlow initialization: the input must be a DataFrame")
    
    @classmethod
    def from_budget(cls, budget_instance):
        # Calculate the number of days and daily cost
        budget_instance['num_days'] = (pd.to_datetime(budget_instance['end_date']) - pd.to_datetime(budget_instance['start_date'])).dt.days + 1
        budget_instance['daily_cost'] = budget_instance['amount'] / budget_instance['num_days']

        # Define columns index
        index_col = pd.MultiIndex.from_frame(budget_instance[["cost_category", "cost_type", "supplier"]])

        # Define time index
        start_date = budget_instance['start_date'].min()
        end_date = budget_instance['end_date'].max()
        index = pd.date_range(start_date, end_date, freq='D', name='date')

        # Initialize cashflow DataFrame
        cashflow_df = pd.DataFrame(index=index, columns=index_col).fillna(0.0).astype(float)

        # Spread costs
        for _, row in budget_instance.iterrows():
            daily_costs = pd.Series([row['daily_cost']] * row['num_days'], 
                                    index=pd.date_range(row['start_date'], periods=row['num_days'], freq='D'))
            cashflow_df.loc[daily_costs.index, (row['cost_category'], row['cost_type'], row['supplier'])] += daily_costs.values

        return cls(cashflow_df)

    # @classmethod
    # def from_csv(cls, csv_file_path):
    #     # Logic to read cash flow data directly from CSV
    #     cashflow_df = ...  # Read and process CSV file to create cash flow DataFrame
    #     return cls(cashflow_df)