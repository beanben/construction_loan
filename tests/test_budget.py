import pandas as pd
import pytest
import pdb
import csv
import os
import re
from datetime import datetime
from construction_loan.budget import (read_csv_to_dataframe, 
                                      validate_columns,
                                      validate_amount_column,
                                      validate_date_format_columns,
                                      validate_start_date_before_end_date,
                                      validate_cost_category_not_empty,
                                      set_project_budget_from_csv,
                                      spread_costs_evenly
                                      )


valid_data_csv = 'tests/valid_data.csv'
missing_columns_data_csv = 'tests/missing_columns_data.csv'
non_numeric_amounts_csv = 'tests/non_numeric_amounts.csv'
invalid_dates_format_csv = 'tests/invalid_dates_format.csv'
invalid_dates_csv = 'tests/invalid_dates.csv'
cost_category_empty_csv = 'tests/cost_category_empty.csv'


# Writing to the CSV files
def write_to_csv(file_name, data_rows):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_rows)

@pytest.fixture(scope="module")
def data_setup():
    valid_data = [
        ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
        ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2020'],
        ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '21/01/2020'],
    ]

    missing_columns_data = [
        ['cost category', 'cost type', 'amount', 'start date', 'end date'],
        ['Acquisition costs', 'Land acquisition costs', '10', '01/01/2020', '01/01/2020'],
    ]

    non_numeric_amounts = [
        ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
        ['Construction costs', 'Build costs', 'builder1','ba', '01/01/2020', '21/01/2020'],
    ]

    invalid_dates_format = [
        ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
        ['Acquisition costs', 'Land acquisition costs', '', '10', '12-26-2020', '12-28-2020'],
    ]

    invalid_dates = [
        ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
        ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2019'],
    ]

    cost_category_empty = [
        ['cost_category','cost type', 'supplier', 'amount', 'start date', 'end date'],
        ['', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2019'],
    ]

    write_to_csv(valid_data_csv, valid_data)
    write_to_csv(missing_columns_data_csv, missing_columns_data)
    write_to_csv(non_numeric_amounts_csv, non_numeric_amounts)
    write_to_csv(invalid_dates_format_csv, invalid_dates_format)
    write_to_csv(invalid_dates_csv, invalid_dates)
    write_to_csv(cost_category_empty_csv, cost_category_empty)

    # yield

    # os.remove(valid_data_csv)
    # os.remove(missing_columns_data_csv)
    # os.remove(non_numeric_amounts_csv)
    # os.remove(invalid_dates_format_csv)
    # os.remove(invalid_dates_csv)
    # os.remove(cost_category_empty_csv)
    


def test_read_csv_to_dataframe(data_setup):
    # Test that the function returns a DataFrame
    df = read_csv_to_dataframe(valid_data_csv)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    for char in df.columns:
        assert re.search(r' ', char) is None

def test_validate_columns(data_setup):
    required_columns = ['cost_category', 'cost_type', 'supplier', 'amount', 'start_date', 'end_date']

    df_missing_columns = read_csv_to_dataframe(missing_columns_data_csv)
    # Test with missing columns
    with pytest.raises(ValueError):
        validate_columns(df_missing_columns, required_columns)

def test_validate_amount_column(data_setup):
    df_non_numeric_amounts = read_csv_to_dataframe(non_numeric_amounts_csv)
    # Test with negative amounts
    with pytest.raises(ValueError):
        validate_amount_column(df_non_numeric_amounts, 'amount')

def test_validate_date_format_columns(data_setup):
    df_invalid_dates_format = read_csv_to_dataframe(invalid_dates_format_csv)
    # Test with invalid date formats
    with pytest.raises(ValueError):
        validate_date_format_columns(df_invalid_dates_format, ['start_date', 'end_date'])

def test_validate_start_date_before_end_date(data_setup):
    df_invalid_dates = read_csv_to_dataframe(invalid_dates_csv)
    # Test with invalid dates
    with pytest.raises(ValueError):
        validate_start_date_before_end_date(df_invalid_dates, 'start_date', 'end_date')

def test_cost_category_not_empty(data_setup):
    df_cost_category_empty = read_csv_to_dataframe(cost_category_empty_csv)
    # Test with empty cost category
    with pytest.raises(ValueError):
        validate_cost_category_not_empty(df_cost_category_empty, 'cost_category')

def test_set_project_budget_from_csv(data_setup):
    df = set_project_budget_from_csv(valid_data_csv)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    for char in df.columns:
        assert re.search(r' ', char) is None

    assert df.at[0, 'cost_category'] == 'Acquisition costs'
    assert df.at[0, 'cost_type'] == 'Land acquisition costs'
    assert pd.isna(df.at[0, 'supplier'])
    assert df.at[0, 'amount'] == 10
    assert df.at[0, 'start_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    assert df.at[0, 'end_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()

    assert df.at[1, 'cost_category'] == 'Construction costs'
    assert df.at[1, 'cost_type'] == 'Build costs'
    assert df.at[1, 'supplier'] == 'builder1'
    assert df.at[1, 'amount'] == 20
    assert df.at[1, 'start_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    assert df.at[1, 'end_date'] == datetime.strptime('2020-01-21', '%Y-%m-%d').date()

def test_spread_costs_evenly():
    # Create a sample DataFrame
    data = {
        'cost_category': ['Category1', 'Category2'],
        'cost_type': ['Type1', 'Type2'],
        'supplier': ['Supplier1', 'Supplier2'],
        'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 5)],
        'end_date': [datetime(2020, 1, 3), datetime(2020, 1, 6)],
        'amount': [300, 200]
    }
    budget_df = pd.DataFrame(data)

    # Convert start_date and end_date to datetime.date objects
    budget_df['start_date'] = pd.to_datetime(budget_df['start_date'])
    budget_df['end_date'] = pd.to_datetime(budget_df['end_date'])

    # Call the function
    result_df = spread_costs_evenly(budget_df)

    # Test 1: Check if result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

    # Test 2: Check the structure of the DataFrame
    assert all(col in result_df.columns for col in budget_df[['cost_category', 'cost_type', 'supplier']].itertuples(index=False, name=None))

    # Test 3: Check the calculation of daily costs
    # For Category1, Type1, Supplier1: 300 / 3 days = 100 per day
    # For Category2, Type2, Supplier2: 200 / 2 days = 100 per day
    assert result_df.loc['2020-01-01', ('Category1', 'Type1', 'Supplier1')] == 100
    assert result_df.loc['2020-01-05', ('Category2', 'Type2', 'Supplier2')] == 100

    # Test 4: Check for correct spreading of costs
    assert result_df.loc['2020-01-02', ('Category1', 'Type1', 'Supplier1')] == 100
    assert result_df.loc['2020-01-04', ('Category2', 'Type2', 'Supplier2')] == 0  # No cost on this day

    #  Test 5: Check that amounts in budget_df are in line with total costs in result_df
    assert budget_df['amount'].sum() == result_df.sum().sum()