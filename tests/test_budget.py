import pandas as pd
import pytest
from construction_loan.budget import set_project_budget_from_csv, spread_costs_evenly
import pdb
import csv
import os

valid_data_csv = 'tests/valid_data.csv'
missing_columns_data_csv = 'tests/missing_columns_data.csv'
invalid_dates_data_csv = 'tests/invalid_dates_data.csv'
negative_amounts_data_csv = 'tests/negative_amounts_data.csv'

# Writing to the CSV files
def write_to_csv(file_name, data_rows):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_rows)

# @pytest.fixture
# def df_budget(data_setup):
#     return set_project_budget_from_csv(valid_data_csv)


# @pytest.fixture
# def df_budget_cashflow_spread_costs_evenly(data_setup):
#     df = set_project_budget_from_csv(valid_data_csv)
#     return spread_costs_evenly(df)


class TestSetProjectBudgetFromCSV:
# tests for set_project_budget_from_csv
    @pytest.fixture(scope="class", autouse=True)
    def data_setup(self):
        valid_data = [
            ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
            ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2020'],
            ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '21/01/2020'],
            ['Construction costs', 'Contingency', 'builder1', '30', '01/05/2020', '05/05/2022'],
            ['Professional fees', 'Development management fee', 'DM', '40', '01/08/2020', '04/08/2022'],
            ['Professional fees', 'Consultants', 'consultant1','50', '10/12/2020', '12/12/2022'],
        ]

        missing_columns_data = [
            ['cost category', 'cost type', 'amount', 'start date', 'end date'],
            ['Acquisition costs', 'Land acquisition costs', '10', '01/01/2020', '01/01/2020'],
            ['Construction costs', 'Build costs','20', '01/01/2020', '20/01/2022'],
            ['Construction costs', 'Contingency','30', '01/05/2020', '05/05/2022'],
            ['Professional fees', 'Development management fee', '40', '01/08/2020', '04/08/2022'],
            ['Professional fees', 'Consultants','50', '10/12/2020', '12/12/2022'],
        ]

        invalid_dates_data = [
            ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
            ['Acquisition costs', 'Land acquisition costs', '', '10', '12/26/2020', '12/28/2020'],
            ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '20/01/2022'],
            ['Construction costs', 'Contingency', 'builder1', '30', '01/05/2020', '05/05/2022'],
            ['Professional fees', 'Development management fee', 'DM', '40', '01/08/2020', '04/08/2022'],
            ['Professional fees', 'Consultants', 'consultant1','50', '10/12/2020', '12/12/2022'],
        ]

        negative_amounts_data = [
            ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
            ['Acquisition costs', 'Land acquisition costs', '', '-10', '01/01/2020', '01/01/2020'],
            ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '20/01/2022'],
            ['Construction costs', 'Contingency', 'builder1', '30', '01/05/2020', '05/05/2022'],
            ['Professional fees', 'Development management fee', 'DM', '40', '01/08/2020', '04/08/2022'],
            ['Professional fees', 'Consultants', 'consultant1','50', '10/12/2020', '12/12/2022'],
        ]

        write_to_csv(valid_data_csv, valid_data)
        write_to_csv(missing_columns_data_csv, missing_columns_data)
        write_to_csv(invalid_dates_data_csv, invalid_dates_data)
        write_to_csv(negative_amounts_data_csv, negative_amounts_data)

        yield

        os.remove(valid_data_csv)
        os.remove(missing_columns_data_csv)
        os.remove(invalid_dates_data_csv)
        os.remove(negative_amounts_data_csv)
   
    def test_set_project_budget_from_csv_valid_data(self):
        # Test with valid data
        df = set_project_budget_from_csv(valid_data_csv)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty


    def test_set_project_budget_from_csv_missing_columns(self):
        # Test with missing columns
        with pytest.raises(ValueError):
            set_project_budget_from_csv(missing_columns_data_csv)


    def test_set_project_budget_from_csv_invalid_dates(self):
        # Test with invalid date formats
        with pytest.raises(ValueError):
            set_project_budget_from_csv(invalid_dates_data_csv)


    def test_set_project_budget_from_csv_negative_amounts(self):
        # Test with negative amounts
        with pytest.raises(ValueError):
            set_project_budget_from_csv(negative_amounts_data_csv)



class TestSpreadCostsEvenly:
    @pytest.fixture(scope="class", autouse=True)
    def data_setup(self):
        valid_data = [
            ['cost category', 'cost type', 'supplier', 'amount', 'start date', 'end date'],
            ['Acquisition costs', 'Land acquisition costs', '', '10', '01/01/2020', '01/01/2020'],
            ['Construction costs', 'Build costs', 'builder1','20', '01/01/2020', '21/01/2020'],
            ['Construction costs', 'Contingency', 'builder1', '30', '01/05/2020', '05/05/2022'],
            ['Professional fees', 'Development management fee', 'DM', '40', '01/08/2020', '04/08/2022'],
            ['Professional fees', 'Consultants', 'consultant1','50', '10/12/2020', '12/12/2022'],
        ]

        write_to_csv(valid_data_csv, valid_data)

        yield

        os.remove(valid_data_csv)

    @pytest.fixture(scope="class")
    def df_budget(self):
        return set_project_budget_from_csv(valid_data_csv)


    @pytest.fixture(scope="class")
    def df_budget_cashflow_spread_costs_evenly(self):
        df = set_project_budget_from_csv(valid_data_csv)
        return spread_costs_evenly(df)


    def test_spread_costs_evenly_valid_data(self, df_budget_cashflow_spread_costs_evenly):
        # Test with valid data
        assert isinstance(df_budget_cashflow_spread_costs_evenly, pd.DataFrame)
        assert not df_budget_cashflow_spread_costs_evenly.empty

    def test_spread_costs_evenly_multi_index(self, df_budget_cashflow_spread_costs_evenly):
        # Test the multi index of the returned DataFrame
        assert isinstance(
            df_budget_cashflow_spread_costs_evenly.columns, pd.MultiIndex)
        assert df_budget_cashflow_spread_costs_evenly.columns.names == [
            'cost_category', 'cost_type', 'supplier']

    def test_spread_costs_evenly_dates(self, df_budget_cashflow_spread_costs_evenly, df_budget):
        # Test that the dadf_budget_cashflow_spread_costs_evenlytes are evenly spread

        for index, col in enumerate(df_budget_cashflow_spread_costs_evenly.columns):
            non_zero_cf = df_budget_cashflow_spread_costs_evenly[col] != 0
            start_date_cf_col = df_budget_cashflow_spread_costs_evenly[col][non_zero_cf].index.min(
            )
            end_date_cf_col = df_budget_cashflow_spread_costs_evenly[col][non_zero_cf].index.max(
            )

            start_date_budget_col = df_budget.at[index, "start_date"]
            end_date_budget_col = df_budget.at[index, "end_date"]

            assert start_date_cf_col == start_date_budget_col
            assert end_date_cf_col == end_date_budget_col


    def test_spread_costs_evenly_amount(self, df_budget_cashflow_spread_costs_evenly):
        # Test that the amounts are evenly spread
        col_tested_1 = ('Acquisition costs', 'Land acquisition costs', '')
        col_tested_2 = ('Construction costs', 'Build costs', 'builder1')

        for col in df_budget_cashflow_spread_costs_evenly.columns:
            non_zero_cf = df_budget_cashflow_spread_costs_evenly[col] != 0
            start_cf_amount = df_budget_cashflow_spread_costs_evenly[col][non_zero_cf].min(
            )
            end_cf_amount = df_budget_cashflow_spread_costs_evenly[col][non_zero_cf].max(
            )

            if col == col_tested_1:
                assert start_cf_amount == 10
                assert end_cf_amount == 10

            if col == col_tested_2:
                assert start_cf_amount == 1
                assert end_cf_amount == 1
