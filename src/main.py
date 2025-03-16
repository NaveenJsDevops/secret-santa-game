import requests
from handle_csv import read_csv, write_csv
from assign_secret_santa import assign_secret_santas

def read_local_csv(file_path):
    """Reads CSV data from a local file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def send_data(api_url, data):
    """Sends processed data to an API via POST request."""
    headers = {'Content-Type': 'application/csv'}  # Adjust as necessary based on API requirements
    response = requests.post(api_url, data=data, headers=headers)
    print(f"Status Code: {response.status_code}, Response: {response.text}")

def main(csv_file_path, api_url_post):
    # Read data from a local CSV file
    csv_data = read_local_csv(csv_file_path)

    # Convert CSV data to list of dictionaries
    employees = read_csv(csv_data)

    # Assign Secret Santas
    assignments = assign_secret_santas(employees)

    # Convert assigned data back to CSV format
    final_csv = write_csv(assignments)

    # Send the final CSV data to an API endpoint
    send_data(api_url_post, final_csv)

if __name__ == '__main__':
    CSV_FILE_PATH = '.csv'
    API_URL_POST = "http://assignments/secret_santa"
    main(CSV_FILE_PATH, API_URL_POST)
