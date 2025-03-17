import pandas as pd
from io import StringIO
import random
import os
from datetime import datetime

def get_previous_year_data():
    """Fetches the Secret Santa assignments from the previous year."""
    last_year = datetime.now().year - 1
    file_path = f"D:\\secret_santa_game_results\\Secret-Santa-Game-Result-{last_year}.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No data file found for the year {last_year}")

    with open(file_path, 'r', encoding='utf-8') as file:
        df = pd.read_csv(file)
    return df.to_dict(orient='records')

def process_employee_data(contents: bytes) -> list:
    """Converts CSV byte content into a list of dictionaries after validating necessary columns."""
    data = StringIO(contents.decode('utf-8'))
    df = pd.read_csv(data)
    required_columns = {'Employee_Name', 'Employee_EmailID'}
    if not required_columns.issubset(df.columns):
        raise ValueError("CSV is missing required columns.")

    return df.to_dict(orient='records')

def create_secret_santa_assignments(current_employees: list) -> list:
    """Creates Secret Santa assignments while avoiding assigning last year's Secret Santa to the same person."""
    try:
        previous_employees = get_previous_year_data()
    except FileNotFoundError as e:
        raise ValueError(str(e))

    previous_year = {emp['Employee_EmailID']: emp.get('Secret_Child_EmailID', None) for emp in previous_employees}
    emp_list = current_employees.copy()
    random.shuffle(emp_list)
    result = []

    for emp in current_employees:
        options = [e for e in emp_list if e['Employee_EmailID'] != emp['Employee_EmailID']
                   and e['Employee_EmailID'] != previous_year.get(emp['Employee_EmailID'], '')]
        if not options:
            raise ValueError("No valid Secret Santa candidates available for all employees; check constraints.")
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
    """Generates a CSV string from a list of dictionaries."""
    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()
