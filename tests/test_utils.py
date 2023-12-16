import pandas as pd
import numpy as np
import pytest
import pdb
import csv
import os
import re
from datetime import datetime
from construction_loan.utils import (read_csv_to_dataframe, 
                                     fill_empty_values_of_string_columns,
                                      validate_columns,
                                      validate_amount_column,
                                      convert_to_valid_date,
                                      validate_date_format_columns,
                                      validate_start_date_before_end_date
                                      )

valid_data_csv = 'tests/valid_data.csv'
valid_data = [
    ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
    ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2020'],
    ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '21/01/2020'],
]

missing_columns_data_csv = 'tests/missing_columns_data.csv'
missing_columns_data = [
    ['cost category', 'cost type', 'amount', 'start date', 'end date'],
    ['Acquisition costs', 'Land acquisition costs', '10', '01/01/2020', '01/01/2020'],
]
non_numeric_amounts_csv = 'tests/non_numeric_amounts.csv'
non_numeric_amounts = [
    ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
    ['Construction costs', 'Build costs', 'builder1','ba', '01/01/2020', '21/01/2020'],
]
invalid_dates_format_csv = 'tests/invalid_dates_format.csv'
invalid_dates_format = [
    ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
    ['Acquisition costs', 'Land acquisition costs', '', '10', '12-26-2020', '12-28-2020'],
]
invalid_dates_csv = 'tests/invalid_dates.csv'
invalid_dates = [
    ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
    ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2019'],
]
# cost_category_empty_csv = 'tests/cost_category_empty.csv'
# cost_category_empty = [
#     ['cost_category','cost type', 'supplier', 'amount', 'start date', 'end date'],
#     ['', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2019'],
# ]

# Writing to the CSV files
def write_to_csv(file_name, data_rows):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_rows)

@pytest.fixture(scope="module")
def data_setup():
    write_to_csv(valid_data_csv, valid_data)
    write_to_csv(missing_columns_data_csv, missing_columns_data)
    write_to_csv(non_numeric_amounts_csv, non_numeric_amounts)
    write_to_csv(invalid_dates_format_csv, invalid_dates_format)
    write_to_csv(invalid_dates_csv, invalid_dates)

    yield

    os.remove(valid_data_csv)
    os.remove(missing_columns_data_csv)
    os.remove(non_numeric_amounts_csv)
    os.remove(invalid_dates_format_csv)
    os.remove(invalid_dates_csv)
    


def test_read_csv_to_dataframe(data_setup):
    # Test that the function returns a DataFrame
    df = read_csv_to_dataframe(valid_data_csv)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    for char in df.columns:
        assert re.search(r' ', char) is None

def test_fill_empty_values_of_string_columns():
    # Create a sample DataFrame
    data = {
        'column1': ['data1', '', 'data3', ' ', np.nan, None, '0.0'],
        'column2': [1, 2, 3, 4, 5, 6, 7],
        'column3': ['data1', 'data2', 'data3', '', ' ', np.nan, '0.0']
    }
    df = pd.DataFrame(data)

    # Columns to fill
    string_columns = ['column1', 'column3']

    # Apply the function
    fill_empty_values_of_string_columns(df, string_columns)

    # Check if the function correctly filled the empty values
    for col in string_columns:
        assert all(x == 'NoData' if x in ['', ' ', np.nan, None, '0.0'] else True for x in df[col]), f"Failed for column {col}"


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

def test_convert_to_valid_date():
    # Test with valid date
    assert convert_to_valid_date('01/01/2020') == datetime.strptime('01/01/2020', '%m/%d/%Y').date()

    # Test with invalid date
    with pytest.raises(ValueError):
        convert_to_valid_date('12-26-2020')


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
