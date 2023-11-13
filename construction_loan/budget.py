import pandas as pd
import numpy as np
import pdb


def set_project_budget_from_csv(csv_file_path: str):
    """
    Reads a CSV file containing the budget for a construction project and returns a validated DataFrame.

    Parameters:
    csv_file_path (str): The file path to a CSV file with the following columns:
                         - 'cost_category' : The category of the cost (e.g., 'Materials', 'Labour')
                         - 'cost_type' : The type of cost
                         - 'supplier' : The supplier of the cost
                         - 'amount' : The amount budgeted for the category
                         - 'start_date' : The start date of the cost
                         - 'end_date' : The end date of the cost

    Returns:
    DataFrame: A pandas DataFrame containing the validated budget data.
    """

    # Read the CSV file into a DataFrame
    budget_df = pd.read_csv(csv_file_path, header=0, na_values=['NA', 'null', '-'])

    required_columns = ['cost_category', 'cost_type', 'supplier',
                        'amount', 'start_date', 'end_date']

    # reformat titles in budget_df.columns to replace spaces with underscores and make lowercase
    budget_df.columns = budget_df.columns.str.replace(' ', '_').str.lower()

    # check if budget_df contains all required columns
    if not all(column in budget_df.columns for column in required_columns):
        raise ValueError(
            f"The DataFrame must contain the following columns: {required_columns}")

    # check that the data in column 'amount' is numeric
    if not pd.api.types.is_numeric_dtype(budget_df['amount']):
        raise ValueError("The 'amount' column must contain numeric data")

    # check that the data in columns 'start_date' and 'end_date' are following the format 'dd/mm/yyyy'
    if not pd.to_datetime(budget_df['start_date'], format='%d/%m/%Y', errors='coerce').notnull().all():
        raise ValueError(
            "The 'start_date' column must contain dates in the format 'dd/mm/yyyy'")
    if not pd.to_datetime(budget_df['end_date'], format='%d/%m/%Y', errors='coerce').notnull().all():
        raise ValueError(
            "The 'end_date' column must contain dates in the format 'dd/mm/yyyy'")

    # check that the data in column 'start_date' is before or equal to the data in column 'end_date'
    if not (pd.to_datetime(budget_df['start_date'], format='%d/%m/%Y') <= pd.to_datetime(budget_df['end_date'], format='%d/%m/%Y')).all():
        raise ValueError(
            "The 'start_date' column must contain dates that are before the dates in the 'end_date' column")
    
    # convert the data in columns 'start_date' and 'end_date' to datetime
    budget_df['start_date'] = pd.to_datetime(budget_df['start_date'], format='%d/%m/%Y')
    budget_df['end_date'] = pd.to_datetime(budget_df['end_date'], format='%d/%m/%Y')

    # check that the data in column 'amount' is positive
    if not (budget_df['amount'] > 0).all():
        raise ValueError("The 'amount' column must contain positive numbers")
    
    # check that the data in column 'cost_category' is not empty
    if not budget_df['cost_category'].notnull().all():
        raise ValueError("The 'cost_category' column must not be empty")
    
    # make sure column 'amount' is float type
    budget_df['amount'] = budget_df['amount'].astype(float)

    # If validation passes, return the DataFrame
    return budget_df


def spread_costs_evenly(budget_df):
    """
    Takes in a budget dataframe and returns a new dataframe with the costs spread evenly between their start and end dates.

    Parameters:
    budget_df (DataFrame): A pandas DataFrame containing the validated budget data.

    Returns:
    DataFrame: A pandas DataFrame containing the spread out budget data.
    """

    cashflow_columns = ['cost_category', 'cost_type', 'supplier', 'amount', 'date']
    cashflow_df = pd.DataFrame(columns=cashflow_columns)

    # define columns index
    index_col = pd.MultiIndex.from_frame(budget_df[["cost_category", "cost_type", "supplier"]])

    # define time index
    start_date = budget_df['start_date'].min()
    end_date = budget_df['end_date'].max()
    index = pd.date_range(start_date, end_date, freq='D', name = 'date')

    cashflow_df = pd.DataFrame(index=index, columns=index_col).fillna(0.0).astype(float)

    # # Loop through each row in the budget dataframe
    for index, row in budget_df.iterrows():

        # Calculate the number of days between the start and end dates
        num_days = (pd.to_datetime(row['end_date'], format='%d/%m/%Y') -
                    pd.to_datetime(row['start_date'], format='%d/%m/%Y')).days
        num_days = 1 if num_days == 0 else num_days
  
        # Calculate the daily cost & allocate to the cashflow dataframe
        daily_cost = row['amount'] / num_days
        cost_series = pd.Series(daily_cost, index=pd.date_range(row['start_date'], row['end_date'], freq='D'))
        cashflow_df.loc[cost_series.index, (row['cost_category'], row['cost_type'], row['supplier'])] = cost_series.values

        # replace NaN with 0
        cashflow_df.fillna(0, inplace=True)


    return cashflow_df

# create a method to group the amounts in the cashflow by calendar months
def group_by_calendar_month(cashflow_df):
    """
    Takes in a cashflow dataframe and returns a new dataframe with the costs grouped by calendar month.

    Parameters:
    cashflow_df (DataFrame): A pandas DataFrame containing the cashflow data.

    Returns:
    DataFrame: A pandas DataFrame containing the grouped cashflow data.
    """
    # # create a new dataframe with the same index as cashflow_df
    # grouped_cashflow_df = pd.DataFrame(index=cashflow_df.index)

    # # create a new column in grouped_cashflow_df called 'total' and set it to 0
    # grouped_cashflow_df['total'] = 0

    # # loop through each column in cashflow_df
    # for column in cashflow_df.columns:
    #     # create a new column in grouped_cashflow_df with the same name as the column in cashflow_df
    #     grouped_cashflow_df[column] = 0
    #     # loop through each month in cashflow_df
    #     for month in cashflow_df.index.month.unique():
    #         # get the sum of the amounts for the month
    #         month_sum = cashflow_df.loc[cashflow_df.index.month == month, column].sum()
    #         # set the value of the new column in grouped_cashflow_df for the month to the sum
    #         grouped_cashflow_df.loc[grouped_cashflow_df.index.month == month, column] = month_sum
    #         # add the sum to the total
    #         grouped_cashflow_df.loc[grouped_cashflow_df.index.month == month, 'total'] += month_sum

    # return grouped_cashflow_df
    return cashflow_df.groupby(cashflow_df.index.to_period('M')).sum()
