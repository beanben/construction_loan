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


def test_budget_from_csv(budget_data_setup):
    budget = Budget.from_csv(valid_data_csv)
    budget_df = budget.df

    # Assertions
    assert isinstance(budget, Budget)
    assert not budget_df.empty

    for char in budget_df.columns:
        assert re.search(r' ', char) is None

    assert budget_df.at[0, 'cost_category'] == 'Acquisition costs'
    assert budget_df.at[0, 'cost_type'] == 'Land acquisition costs'
    assert budget_df.at[0, 'supplier'] == 'NoData'
    assert budget_df.at[0, 'amount'] == 10
    assert budget_df.at[0, 'start_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    assert budget_df.at[0, 'end_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()

    assert budget_df.at[1, 'cost_category'] == 'Construction costs'
    assert budget_df.at[1, 'cost_type'] == 'Build costs'
    assert budget_df.at[1, 'supplier'] == 'builder1'
    assert budget_df.at[1, 'amount'] == 20
    assert budget_df.at[1, 'start_date'] == datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    assert budget_df.at[1, 'end_date'] == datetime.strptime('2020-01-21', '%Y-%m-%d').date()

def test_total_cost(budget_data_setup):
    budget = Budget.from_csv(valid_data_csv)
    assert budget.total_cost() == 30

def test_total_cost_by_level():
    budget = Budget.from_csv(valid_data_csv)

    # Call the method
    result = budget.total_cost_by_level('cost_type')

    # Expected result
    expected_data = {
        'Land acquisition costs': 10,
        'Build costs': 20,
        'Total': 30
    }
    expected_df = pd.Series(expected_data, name='amount')
    expected_df.index.name = 'cost_type'

    # Check if the result matches the expected output
    pd.testing.assert_series_equal(result, expected_df)