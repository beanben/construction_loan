
import pytest
from construction_loan.cashflow import Cashflow
from construction_loan.budget import Budget
import csv
import os
import pdb
import pandas as pd

valid_budget_data_csv = 'tests/valid_budget_data.csv'
valid_budget_data = [
    ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
    ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2020'],
    ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '21/01/2020'],
]

csv_data_csv = 'tests/csv_data.csv'
csv_data = [
    ['cost category', 'cost type', 'supplier', '09/12/20', '03/02/21', '24/02/21'],
    ['Acquisition costs', 'Site acquisition', '', '10', '', ''],
    ['Construction costs', 'Build costs', 'builder1', '20', '30', '40']
]

# Writing to the CSV files
def write_to_csv(file_name, data_rows):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_rows)

@pytest.fixture(scope='module')
def cashflow_data_setup():
    # Setup code to create CSV
    write_to_csv(valid_budget_data_csv, valid_budget_data)
    write_to_csv(csv_data_csv, csv_data)

    yield

    os.remove(valid_budget_data_csv)
    os.remove(csv_data_csv)

def test_cashflow_from_budget(cashflow_data_setup):
    budget = Budget.from_csv(valid_budget_data_csv) # Create a sample budget instance
    cashflow = Cashflow.from_budget(budget)

    assert isinstance(cashflow, Cashflow)
    assert cashflow.total_cost() == budget.total_cost()
    
def test_cashflow_from_csv(cashflow_data_setup):
    cashflow = Cashflow.from_csv(csv_data_csv)

    assert isinstance(cashflow, Cashflow)
    assert isinstance(cashflow.df, pd.DataFrame)
    assert cashflow.df.shape == (3, 2)

def test_total_cost(cashflow_data_setup):
    cashflow = Cashflow.from_csv(csv_data_csv)
    # Call the method
    result = cashflow.total_cost()
    # Expected result
    expected_result = 100.0
    # Assert the result
    assert result == expected_result

def test_costs_grouped_by_level(cashflow_data_setup):
    cashflow = Cashflow.from_csv(csv_data_csv)

    # Call the method
    result = cashflow.costs_grouped_by_level('cost_type')

    # Expected result
    expected_data = {
        'Site acquisition': [10.0, 0.0, 0.0],
        'Build costs': [20.0, 30.0, 40.0],
        'total': [30.0, 30.0, 40.0]
    }
    expected_df = pd.DataFrame(expected_data, index=[
        pd.to_datetime('09/12/20', format='%d/%m/%y').date(),
        pd.to_datetime('03/02/21', format='%d/%m/%y').date(),
        pd.to_datetime('24/02/21', format='%d/%m/%y').date()
    ])
    expected_df.columns.name = 'cost_type'

    pd.testing.assert_frame_equal(result, expected_df)

def test_costs_summary(cashflow_data_setup):
    cashflow = Cashflow.from_csv(csv_data_csv)

    # Call the method
    result = cashflow.costs_summary()

    # Expected result (nth largest re ordered)
    expected_data = {
        'Construction costs': [20.0, 30.0, 40.0],
        'Acquisition costs': [10.0, 0.0, 0.0],
        'total': [30.0, 30.0, 40.0]
    }
    expected_df = pd.DataFrame(expected_data, index=[
        pd.to_datetime('09/12/20', format='%d/%m/%y').date(),
        pd.to_datetime('03/02/21', format='%d/%m/%y').date(),
        pd.to_datetime('24/02/21', format='%d/%m/%y').date()
    ])

    pd.testing.assert_frame_equal(result, expected_df)

# def test_get_costs