
import pytest
from construction_loan.cashflow import CashFlow
from construction_loan.budget import Budget
import csv
import os
import pdb

valid_budget_data_csv = 'tests/valid_budget_data.csv'
valid_budget_data = [
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
def cashflow_data_setup():
    # Setup code to create CSV
    write_to_csv(valid_budget_data_csv, valid_budget_data)

    yield

    os.remove(valid_budget_data_csv)

def test_cashflow_from_budget(cashflow_data_setup):
    budget = Budget(valid_budget_data_csv) # Create a sample budget instance
    cashflow = CashFlow.from_budget(budget)
    
    # Assert that the cash flow object is created correctly
    assert isinstance(cashflow, CashFlow)
    # pdb.set_trace() # to debug

    # Assert if the sum of all amounts in cashflow is equal to the sum of all amounts in budget
    assert cashflow.total_cost() == budget.total_cost()
    
# def test_cashflow_from_csv():
#     csv_file_path = '/path/to/cashflow.csv'  # Replace with actual file path
#     cashflow = CashFlow.from_csv(csv_file_path)
    
#     # Assert that the cash flow object is created correctly
#     assert isinstance(cashflow, CashFlow)
#     assert cashflow.data.shape[0] > 0  # Assuming `data` attribute in CashFlow class

def test_cashflow_calculation(cashflow_data_setup):
    budget = Budget(valid_budget_data_csv) # Create a sample budget instance
    cashflow = CashFlow.from_budget(budget)
    
    # Perform some calculations on the cash flow data
    total_cost = cashflow.total_cost()
    
    # Assert the calculated values
    assert total_cost == 30

# # to debug
# cashflow_data_setup()
# test_cashflow_from_budget(cashflow_data_setup)