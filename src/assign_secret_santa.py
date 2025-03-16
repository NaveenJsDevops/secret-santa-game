import random

def assign_secret_santas(employees):
    current_year = {}
    previous_year = {emp['Employee_EmailID']: emp['Secret_Child_EmailID'] for emp in employees}
    emp_list = employees.copy()

    for emp in employees:
        options = [e for e in emp_list if e['Employee_EmailID'] != emp['Employee_EmailID']
                   and e['Employee_EmailID'] != previous_year.get(emp['Employee_EmailID'])]
        selected = random.choice(options)
        emp_list.remove(selected)
        current_year[emp['Employee_EmailID']] = selected['Employee_EmailID']

    result = [
        {
            'Employee_Name': emp['Employee_Name'],
            'Employee_EmailID': emp['Employee_EmailID'],
            'Secret_Child_Name': next(e['Employee_Name'] for e in employees if e['Employee_EmailID'] == current_year[emp['Employee_EmailID']]),
            'Secret_Child_EmailID': current_year[emp['Employee_EmailID']]
        }
        for emp in employees
    ]
    return result
