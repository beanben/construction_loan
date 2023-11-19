import pytest
import csv
from construction_loan.budget import Budget
import pandas as pd
import re
from datetime import datetime
import os
import pdb

valid_data_csv = 'tests/valid_data.csv'
valid_data = [
    ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
    ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2020'],
    ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '21/01/2020'],
]

# Writing to the CSV files
def write_to_csv(file_name, data_rows):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_rows)

@pytest.fixture(scope='module')
def budget_data_setup():
    # Setup code to create CSV
    write_to_csv(valid_data_csv, valid_data)

    yield

    os.remove(valid_data_csv)


def test_set_project_budget_from_csv(budget_data_setup):
    # Instantiate Budget here, after the fixture has run
    budget = Budget(valid_data_csv).budget_df

    # Assertions
    assert isinstance(budget, pd.DataFrame)
    assert not budget.empty

    for char in budget.columns:
        assert re.search(r' ', char) is None

    assert budget.at[0, 'cost_category'] == 'Acquisition costs'
    assert budget.at[0, 'cost_type'] == 'Land acquisition costs'
    assert pd.isna(budget.at[0, 'supplier'])
    assert budget.at[0, 'amount'] == 10
    assert budget.at[0, 'start_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    assert budget.at[0, 'end_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()

    assert budget.at[1, 'cost_category'] == 'Construction costs'
    assert budget.at[1, 'cost_type'] == 'Build costs'
    assert budget.at[1, 'supplier'] == 'builder1'
    assert budget.at[1, 'amount'] == 20
    assert budget.at[1, 'start_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    assert budget.at[1, 'end_date'] == datetime.strptime('2020-01-21', '%Y-%m-%d').date()

# test total_cost method
def test_total_cost(budget_data_setup):
    budget = Budget(valid_data_csv)
    assert budget.total_cost() == 30






# # def test_spread_costs_evenly():
#     # Create a sample DataFrame
#     data = {
#         'cost_category': ['Category1', 'Category2'],
#         'cost_type': ['Type1', 'Type2'],
#         'supplier': ['Supplier1', 'Supplier2'],
#         'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 5)],
#         'end_date': [datetime(2020, 1, 3), datetime(2020, 1, 6)],
#         'amount': [300, 200]
#     }
#     budget_df = pd.DataFrame(data)

#     # Convert start_date and end_date to datetime.date objects
#     budget_df['start_date'] = pd.to_datetime(budget_df['start_date'])
#     budget_df['end_date'] = pd.to_datetime(budget_df['end_date'])

#     # Call the function
#     result_df = spread_costs_evenly(budget_df)

#     # Test 1: Check if result is a DataFrame
#     assert isinstance(result_df, pd.DataFrame)

#     # Test 2: Check the structure of the DataFrame
#     assert all(col in result_df.columns for col in budget_df[['cost_category', 'cost_type', 'supplier']].itertuples(index=False, name=None))

#     # Test 3: Check the calculation of daily costs
#     # For Category1, Type1, Supplier1: 300 / 3 days = 100 per day
#     # For Category2, Type2, Supplier2: 200 / 2 days = 100 per day
#     assert result_df.loc['2020-01-01', ('Category1', 'Type1', 'Supplier1')] == 100
#     assert result_df.loc['2020-01-05', ('Category2', 'Type2', 'Supplier2')] == 100

#     # Test 4: Check for correct spreading of costs
#     assert result_df.loc['2020-01-02', ('Category1', 'Type1', 'Supplier1')] == 100
#     assert result_df.loc['2020-01-04', ('Category2', 'Type2', 'Supplier2')] == 0  # No cost on this day

#     #  Test 5: Check that amounts in budget_df are in line with total costs in result_df
#     assert budget_df['amount'].sum() == result_df.sum().sum()