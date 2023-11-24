import pandas as pd
from construction_loan.utils import time_execution, dataframe_to_csv

class Cashflow:
    billing_period = 'M'

    def __init__(self, data):
            if isinstance(data, pd.DataFrame):
                self.df = data
            else:
                raise ValueError("Invalid input type for CashFlow initialization: the input must be a DataFrame")
    
    @classmethod
    @time_execution
    def from_budget(cls, budget_instance):

        # get the budget dataframe
        budget_df = budget_instance.df.copy()

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

        
        # group the cashflow by billing period
        cashflow_df = cashflow_df.resample(cls.billing_period).sum()

        return cls(cashflow_df)

    def total_cost(self):
        return self.df.sum().sum()

    def costs_grouped_by_level(self, level):
        df = self.df.T.groupby(level=level).sum().T
        df['total'] = df.sum(axis=1)
        return df
    
    # summarise the cashflow by key cost_category: acquisition costs, construction costs and put the rest in a new cateogry called other costs
    def costs_summary(self):
        # Group the cashflow by cost_category and sum
        grouped_df = self.df.T.groupby(level='cost_category').sum().T

        # Calculate the total for each cost_category
        total_by_category = grouped_df.sum(axis=0)

        # Identify the top 4 categories
        top4_categories = total_by_category.nlargest(4).index

       # Create a new DataFrame to store the summarized data
        cashflow_df_summary = pd.DataFrame()

        # Add the top 4 categories as they are
        for category in top4_categories:
            cashflow_df_summary[category] = grouped_df[category]

        # group from the grouped_df the rest of the categories in a new category called other
        other_data = grouped_df.loc[:, ~grouped_df.columns.isin(top4_categories)].copy()
        cashflow_df_summary['other'] = other_data.sum(axis=1)
        
        # add a total column
        cashflow_df_summary['total'] = cashflow_df_summary.sum(axis=1)

        return cashflow_df_summary

    
    def df_to_csv(self, csv_file_path):
        dataframe_to_csv(self.df, csv_file_path)
    
