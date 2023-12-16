import pandas as pd
from datetime import date
from construction_loan.utils import (read_csv_to_dataframe,
                                     validate_columns,
                                     validate_amount_column,
                                     validate_date_format_columns,
                                     validate_start_date_before_end_date,
                                     fill_empty_values_of_string_columns,
                                     convert_to_valid_date,
                                     time_execution)


class ProjectCosts:
    billing_period = 'M'

    def __init__(self, cashflow):
        if isinstance(cashflow, pd.DataFrame):
            self.cashflow = cashflow
        else:
            raise ValueError(
                "Invalid input type for ProjectCosts initialization: the input must be a DataFrame")

    @classmethod
    def from_budget(cls, csv_file_path: str) -> 'ProjectCosts':
        fundable_costs = cls._from_budget_to_fundable_costs(csv_file_path)
        cashflow = cls._fundable_costs_cashflow(fundable_costs)
        return cls(cashflow)

    @staticmethod
    def _from_budget_to_fundable_costs(csv_file_path: str) -> pd.DataFrame:
        # Read the CSV file into a DataFrame
        budget_df = read_csv_to_dataframe(csv_file_path)

        # Define the required columns
        required_columns = ['cost_category', 'cost_type',
                            'supplier', 'amount', 'start_date', 'end_date']

        # fill in the emptuy values of cost_category, cost_type and supplier with 'NoData'
        budget_df[['cost_category', 'cost_type', 'supplier']] = budget_df[[
            'cost_category', 'cost_type', 'supplier']].astype(str)
        fill_empty_values_of_string_columns(
            budget_df, ['cost_category', 'cost_type', 'supplier'])

        # Perform validations
        validate_columns(budget_df, required_columns)
        validate_amount_column(budget_df, 'amount')
        validate_date_format_columns(budget_df, ['start_date', 'end_date'])
        validate_start_date_before_end_date(
            budget_df, 'start_date', 'end_date')
        # validate_cost_category_not_empty(budget_df, 'cost_category')

        return budget_df

    @staticmethod
    def _fundable_costs_cashflow(budget_df_init: pd.DataFrame) -> pd.DataFrame:
        # get the budget dataframe
        budget_df = budget_df_init.copy()

        # Calculate the number of days and daily cost
        budget_df['num_days'] = (pd.to_datetime(
            budget_df['end_date']) - pd.to_datetime(budget_df['start_date'])).dt.days + 1
        budget_df['daily_cost'] = (budget_df['amount'] / budget_df['num_days'])

        # Define columns index
        index_col = pd.MultiIndex.from_frame(
            budget_df[["cost_category", "cost_type", "supplier"]])

        # Define time index
        start_date = budget_df['start_date'].min()
        end_date = budget_df['end_date'].max()
        index = pd.date_range(start_date, end_date, freq='D', name='date')

        # Initialize cashflow DataFrame
        cashflow_df = pd.DataFrame(
            index=index, columns=index_col).fillna(0.0).astype(float)

        # Spread costs
        for _, row in budget_df.iterrows():
            daily_costs = pd.Series([row['daily_cost']] * row['num_days'],
                                    index=pd.date_range(row['start_date'], periods=row['num_days'], freq='D'))

            # amend the last days' cost with the difference between the total cost and the sum of the daily costs, to ensure rouding errors are accounted for
            daily_costs.iloc[-1] += row['amount'] - daily_costs.sum()
            cashflow_df.loc[daily_costs.index, (
                row['cost_category'], row['cost_type'], row['supplier'])] += daily_costs.values

        # group the cashflow by billing period
        cashflow_df = cashflow_df.resample(self.billing_period).sum().round(2)

        return cashflow_df

    @classmethod
    def from_cashflow(cls, csv_file_path: str) -> 'ProjectCosts':
        # Read the CSV file with the first three rows as header for MultiIndex
        df = read_csv_to_dataframe(csv_file_path)
        fill_empty_values_of_string_columns(
            df, ['cost_category', 'cost_type', 'supplier'])
        df = df.transpose()

        # Define columns index
        column_names = df.iloc[:3].index.values
        column_names = [name.strip().replace(' ', '_').lower()
                        for name in column_names]
        index_col = pd.MultiIndex.from_frame(
            df.iloc[:3].transpose(), names=column_names)

        # Define time index
        dates = df.index.values[3:]
        index_dates = [convert_to_valid_date(date_str) for date_str in dates]

        # Initialize cashflow DataFrame
        cashflow_df = pd.DataFrame(
            index=index_dates, columns=index_col).fillna(0.0).astype(float)

        # add the data to the cashflow_df
        df_data = df.iloc[3:].copy()
        df_data.index = cashflow_df.index
        for index, column_name in enumerate(cashflow_df.columns):
            # convert the data to numeric
            data_as_string = df_data.iloc[:, index].astype(str)
            data_no_comma = data_as_string.str.replace(',', '')
            costs = pd.to_numeric(data_no_comma, errors='coerce')

            # add the data to the cashflow_df
            cashflow_df[column_name] = costs

        return cls(cashflow_df)

    def list_costs(self):
        return self.cashflow.sum().sum()

    def grouped_by_level(self, level):
        df = self.cashflow.T.groupby(level=level, sort=False).sum().T
        df['total'] = df.sum(axis=1)
        return df

    def grouped_by_largest(self):
        # Group the cashflow by cost_category and sum
        grouped_df = self.cashflow.T.groupby(
            level='cost_category', sort=False).sum().T

        # Calculate the total for each cost_category
        total_by_category = grouped_df.sum(axis=0)

        # Identify the top 4 categories
        top4_categories = total_by_category.nlargest(4).index

       # Create a new DataFrame to store the summarized data
        cashflow_df_summary = pd.DataFrame()

        # Add the top 4 categories as they are
        for category in top4_categories:
            cashflow_df_summary[category] = grouped_df[category]

        # Check if there are more categories beyond the top 4
        if len(total_by_category) > 4:
            # group from the grouped_df the rest of the categories in a new category called other
            other_data = grouped_df.loc[:, ~grouped_df.columns.isin(
                top4_categories)].copy()
            cashflow_df_summary['other'] = other_data.sum(axis=1)

        # add a total column
        cashflow_df_summary['total'] = cashflow_df_summary.sum(axis=1)

        return cashflow_df_summary
