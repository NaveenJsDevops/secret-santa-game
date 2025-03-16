import csv
from io import StringIO

def read_csv(csv_content):
    file = StringIO(csv_content)
    reader = csv.DictReader(file)
    return list(reader)

def write_csv(data_dicts):
    output = StringIO()
    fields = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for data in data_dicts:
        writer.writerow(data)
    return output.getvalue()
