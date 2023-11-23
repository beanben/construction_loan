import pandas as pd
import pdb
import time
import functools

def time_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution of {func.__name__} took {end_time - start_time} seconds")
        return result
    return wrapper

def read_csv_to_dataframe(csv_file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a DataFrame.

    Parameters:
    csv_file_path (str): Path to the CSV file.

    Returns:
    DataFrame: The read DataFrame.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file_path, header=0, na_values=['NA', 'null', '-'])
    
    # Format column names
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
    return df

def validate_columns(budget_df: pd.DataFrame, required_columns: list) -> None:
    """
    Validates if the required columns are present in the DataFrame.

    Parameters:
    budget_df (DataFrame): The DataFrame to validate.
    required_columns (list): List of required column names.

    Raises:
    ValueError: If required columns are missing.
    """
    missing_columns = [col for col in required_columns if col not in budget_df.columns]
    if missing_columns:
        raise ValueError(f"The DataFrame is missing the following required columns: {missing_columns}")

def validate_amount_column(budget_df: pd.DataFrame, amount_column: str) -> None:
    """
    Validates if the data in the amount column is numeric and converts string representations of float numbers to float.

    Parameters:
    budget_df (DataFrame): The DataFrame to validate.
    amount_column (str): The name of the amount column.

    Raises:
    ValueError: If the amount column does not contain numeric data or contains invalid formats.
    """
    # Handle columns that are already in the correct numeric format
    if pd.api.types.is_numeric_dtype(budget_df[amount_column]):
        return

    try:
        # Convert string representations of numbers (with commas and spaces) to float
        budget_df[amount_column] = budget_df[amount_column].replace(',', '', regex=True).str.strip()
        budget_df[amount_column] = pd.to_numeric(budget_df[amount_column], errors='raise')
        # print("before conversion: ", budget_df[amount_column].dtype)
        budget_df[amount_column] = budget_df[amount_column].astype(float)
        # print("after conversion: ", budget_df[amount_column].dtype)
    except ValueError:
        # Raise an error if conversion fails due to invalid formats
        raise ValueError(f"The '{amount_column}' column must contain valid numeric data")

    # Additional check: Ensure the column is now of a numeric dtype
    if not pd.api.types.is_numeric_dtype(budget_df[amount_column]):
        raise ValueError(f"The '{amount_column}' column must contain numeric data")

     
def validate_date_format_columns(budget_df: pd.DataFrame, date_columns: list) -> None:
    """
    Validates if the data in the date columns are in acceptable date formats.

    Parameters:
    budget_df (DataFrame): The DataFrame to validate.
    date_columns (list): List of date column names.

    Raises:
    ValueError: If the date columns do not contain dates in acceptable formats.
    """
    acceptable_formats = ['%d-%b-%y', '%d-%b-%Y', '%d/%m/%y', '%d/%m/%Y']
    
    for date_column in date_columns:
        original_column = budget_df[date_column].copy()
        for fmt in acceptable_formats:
            temp_column = pd.to_datetime(original_column, format=fmt, errors='coerce')
            if not temp_column.isnull().all():
                break
        
            
        if temp_column.isnull().any():
            raise ValueError(f"The '{date_column}' column must contain dates in acceptable formats: 'dd-MMM-yy', 'dd-MMM-yyyy', 'dd/mm/yy', or 'dd/mm/yyyy'")

        budget_df[date_column] = temp_column.dt.date

        
def validate_start_date_before_end_date(budget_df: pd.DataFrame, start_date_column: str, end_date_column: str) -> None:
    """
    Validates if the data in the start date column is before or equal to the data in the end date column.

    Parameters:
    budget_df (DataFrame): The DataFrame to validate.
    start_date_column (str): The name of the start date column.
    end_date_column (str): The name of the end date column.

    Raises:
    ValueError: If the start date column contains dates that are after the dates in the end date column.
    """
    if not (budget_df[start_date_column] <= budget_df[end_date_column]).all():
        raise ValueError(f"The '{start_date_column}' column must contain dates that are before or equal to the dates in the '{end_date_column}' column")
   
def validate_cost_category_not_empty(budget_df: pd.DataFrame, cost_category_column: str) -> None:
    """
    Validates if the data in the cost category column is not empty.

    Parameters:
    budget_df (DataFrame): The DataFrame to validate.
    cost_category_column (str): The name of the cost category column.

    Raises:
    ValueError: If the cost category column is empty.
    """
    if budget_df[cost_category_column].isnull().any():
        raise ValueError(f"The '{cost_category_column}' column must not be empty")

def dataframe_to_csv(df: pd.DataFrame, csv_file_path: str) -> None:
    """
    Writes a DataFrame to a CSV file.

    Parameters:
    df (DataFrame): The DataFrame to write.
    csv_file_path (str): Path to the CSV file.
    """
    df.to_csv(csv_file_path, index=False)