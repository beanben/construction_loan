import pandas as pd
from construction_loan.utils import (read_csv_to_dataframe, 
                    validate_columns, 
                    validate_amount_column, 
                    validate_date_format_columns,
                    validate_start_date_before_end_date,
                    validate_cost_category_not_empty,
                    time_execution)
                   

class Budget:
    def __init__(self, data):
            if isinstance(data, pd.DataFrame):
                self.df = data
            else:
                raise ValueError("Invalid input type for Budget initialization: the input must be a DataFrame")
    
    @classmethod
    @time_execution
    def from_csv(cls, csv_file_path: str) -> pd.DataFrame:
        # Read the CSV file into a DataFrame
        budget_df = read_csv_to_dataframe(csv_file_path)

        # Define the required columns
        required_columns = ['cost_category', 'cost_type', 'supplier', 'amount', 'start_date', 'end_date']

        # Perform validations
        validate_columns(budget_df, required_columns)
        validate_amount_column(budget_df, 'amount')
        validate_date_format_columns(budget_df, ['start_date', 'end_date'])
        validate_start_date_before_end_date(budget_df, 'start_date', 'end_date')
        validate_cost_category_not_empty(budget_df, 'cost_category')

        return cls(budget_df)
    
    def total_cost(self):
        return self.df.amount.sum()
    
    def total_cost_by_level(self, category):
        df = self.df.groupby(by=category).amount.sum()

        # add a total row
        df.loc['Total'] = df.sum()
        return df