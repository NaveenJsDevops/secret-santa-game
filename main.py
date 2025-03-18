import io
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List

from starlette.responses import FileResponse

from src.secret_santa_manager import process_employee_data, create_secret_santa_assignments, generate_csv_from_data
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime

app = FastAPI()

# Define the base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory where static files are stored
static_dir = os.path.join(BASE_DIR, 'static')

# Serve static files from the '/static' directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Route to serve index.html at "/"
@app.get("/")
async def serve_ui():
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.post("/upload/employee_list")
async def upload_employee_list(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload employee CSV files and generate Secret Santa assignments.
    Accepts one file for current year employees and optionally another for last year's results.
    """
    employee_data_file = None
    previous_year_data_file = None

    # Determine the role of each uploaded file based on filename
    for file in files:
        if 'Employee-List.csv' in file.filename:
            employee_data_file = file  # Current year employee data
        elif 'Secret-Santa-Game-Result' in file.filename:
            previous_year_data_file = file  # Previous year results

    # Validate the presence of the current year employee data
    if not employee_data_file:
        raise HTTPException(status_code=400, detail="The current employee list must be provided.")

    # If the previous year data file is not provided, treat previous employees as an empty list
    if not previous_year_data_file:
        previous_employees = []
    else:
        previous_results_contents = await previous_year_data_file.read()
        previous_employees = process_employee_data(previous_results_contents)

    # Read the contents of the current year file
    current_employee_contents = await employee_data_file.read()
    try:
        # Process data into structured records
        current_employees = process_employee_data(current_employee_contents)

        # Generate Secret Santa assignments based on the current and previous data
        secret_santa_assignments = create_secret_santa_assignments(current_employees, previous_employees)

        # Prepare CSV data from the assignments
        current_year = datetime.now().year
        filename = f"Secret-Santa-Result-{current_year}.csv"
        csv_data = generate_csv_from_data(secret_santa_assignments)
        headers = {"Content-Disposition": f"attachment; filename={filename}"}

        # Stream the CSV data as a response
        return StreamingResponse(io.StringIO(csv_data), media_type="text/csv", headers=headers)
    except Exception as e:
        # Handle exceptions with a generic server error message
        raise HTTPException(status_code=500, detail=f"Failed to process data and generate CSV: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
