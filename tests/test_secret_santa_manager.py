import csv

import pytest
from src.secret_santa_manager import (
    process_employee_data,
    create_secret_santa_assignments,
    generate_csv_from_data
)

# Sample CSV content for testing
VALID_CSV_CONTENT = b"Employee_Name,Employee_EmailID\nAlice,alice@example.com\nBob,bob@example.com\nCharlie,charlie@example.com"
PREVIOUS_YEAR_DATA = [
    {'Employee_Name': 'Alice', 'Employee_EmailID': 'alice@example.com', 'Secret_Child_EmailID': 'bob@example.com'}
]
MISSING_COLUMN_CSV_CONTENT = b"Employee_Name\nAlice\nBob"
EMPTY_CSV_CONTENT = b""

# ================================
# Tests for process_employee_data
# ================================
def test_process_valid_employee_data():
    """Test processing a valid employee CSV file."""
    expected_result = [
        {'Employee_Name': 'Alice', 'Employee_EmailID': 'alice@example.com'},
        {'Employee_Name': 'Bob', 'Employee_EmailID': 'bob@example.com'},
        {'Employee_Name': 'Charlie', 'Employee_EmailID': 'charlie@example.com'}
    ]
    result = process_employee_data(VALID_CSV_CONTENT)
    assert result == expected_result


def test_process_employee_data_missing_columns():
    """Test handling missing columns in the CSV file."""
    with pytest.raises(ValueError) as excinfo:
        process_employee_data(MISSING_COLUMN_CSV_CONTENT)
    assert "missing the following required columns: Employee_EmailID" in str(excinfo.value)

def test_process_employee_data_empty_file():
    """Test handling an empty CSV file."""
    with pytest.raises(ValueError) as excinfo:
        process_employee_data(EMPTY_CSV_CONTENT)
    assert "The provided CSV file is empty and cannot be processed." in str(excinfo.value)

# ===========================================
# Tests for create_secret_santa_assignments
# ===========================================
def test_create_valid_secret_santa_assignments():
    """Test generating Secret Santa assignments with valid employee data."""
    current_employees = process_employee_data(VALID_CSV_CONTENT)
    assignments = create_secret_santa_assignments(current_employees, PREVIOUS_YEAR_DATA)

    assert len(assignments) == 3  # Ensure all three employees are assigned
    for assignment in assignments:
        assert 'Secret_Child_Name' in assignment
        assert 'Secret_Child_EmailID' in assignment
        assert assignment['Employee_EmailID'] != assignment['Secret_Child_EmailID']  # Ensure no self-assignment


def test_no_valid_candidates():
    """Test scenario where an employee has no valid candidates for Secret Santa."""
    single_employee_list = [
        {'Employee_Name': 'Alice', 'Employee_EmailID': 'alice@example.com'}
    ]
    with pytest.raises(ValueError) as excinfo:
        create_secret_santa_assignments(single_employee_list, [])
    assert "No valid Secret Santa candidates available" in str(excinfo.value)

# ================================
# Tests for generate_csv_from_data
# ================================
def test_generate_csv_from_data():
    """Test generating a CSV string from assignment data."""
    data = [
        {'Employee_Name': 'Alice', 'Employee_EmailID': 'alice@example.com', 'Secret_Child_Name': 'Bob', 'Secret_Child_EmailID': 'bob@example.com'},
        {'Employee_Name': 'Bob', 'Employee_EmailID': 'bob@example.com', 'Secret_Child_Name': 'Charlie', 'Secret_Child_EmailID': 'charlie@example.com'},
        {'Employee_Name': 'Charlie', 'Employee_EmailID': 'charlie@example.com', 'Secret_Child_Name': 'Alice', 'Secret_Child_EmailID': 'alice@example.com'}
    ]

    result_csv = generate_csv_from_data(data)

    expected_csv = """Employee_Name,Employee_EmailID,Secret_Child_Name,Secret_Child_EmailID
Alice,alice@example.com,Bob,bob@example.com
Bob,bob@example.com,Charlie,charlie@example.com
Charlie,charlie@example.com,Alice,alice@example.com
"""

    # Convert CSV strings into lists of dictionaries for comparison
    result_reader = list(csv.DictReader(result_csv.strip().split("\n")))
    expected_reader = list(csv.DictReader(expected_csv.strip().split("\n")))

    assert result_reader == expected_reader


# ================================
# Running Tests with Pytest
# ================================
if __name__ == "__main__":
    pytest.main()
