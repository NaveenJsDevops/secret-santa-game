import pandas as pd
from io import StringIO
import random

def process_employee_data(contents: bytes) -> list:
    """
    Converts CSV byte content into a list of dictionaries while validating necessary columns.

    Args:
        contents (bytes): The content of a CSV file in bytes.

    Returns:
        list: A list of dictionaries, each representing a row from the CSV.

    Raises:
        ValueError: If the CSV is missing required columns.
    """
    data = StringIO(contents.decode('utf-8'))
    try:
        df = pd.read_csv(data)
    except pd.errors.EmptyDataError:
        raise ValueError("The provided CSV file is empty and cannot be processed.")

    required_columns = {'Employee_Name', 'Employee_EmailID'}
    if not required_columns.issubset(df.columns):
        missing_columns = required_columns - set(df.columns)
        raise ValueError(f"The CSV file is missing the following required columns: {', '.join(missing_columns)}")

    return df.to_dict(orient='records')

def create_secret_santa_assignments(current_employees: list, previous_employees: list) -> list:
    """
    Creates Secret Santa assignments ensuring no employee is assigned their last year's Secret Santa.

    Args:
        current_employees (list): List of dictionaries containing current year employee data.
        previous_employees (list): List of dictionaries containing previous year Secret Santa data.

    Returns:
        list: A list of Secret Santa assignments.

    Raises:
        ValueError: If no valid Secret Santa candidate is available for any employee.
    """
    previous_year = {emp['Employee_EmailID']: emp.get('Secret_Child_EmailID', '') for emp in previous_employees}
    emp_list = current_employees.copy()
    random.shuffle(emp_list)
    result = []

    for emp in current_employees:
        options = [e for e in emp_list if e['Employee_EmailID'] != emp['Employee_EmailID']
                   and e['Employee_EmailID'] != previous_year.get(emp['Employee_EmailID'], '')]
        if not options:
            raise ValueError(f"No valid Secret Santa candidates available for employee {emp['Employee_Name']} (ID: {emp['Employee_EmailID']}).")
        selected = random.choice(options)
        emp_list.remove(selected)
        result.append({
            'Employee_Name': emp['Employee_Name'],
            'Employee_EmailID': emp['Employee_EmailID'],
            'Secret_Child_Name': selected['Employee_Name'],
            'Secret_Child_EmailID': selected['Employee_EmailID']
        })
    return result

def generate_csv_from_data(data: list) -> str:
    """
    Generates a CSV string from provided data.

    Args:
        data (list): List of dictionaries to be converted into a CSV string.

    Returns:
        str: A CSV string formatted from the input data.
    """
    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()
