from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from src.secret_santa_manager import process_employee_data, create_secret_santa_assignments, generate_csv_from_data

app = FastAPI()

@app.post("/upload/employee_list")
async def upload_employee_list(file: UploadFile = File(...)):
    if file.filename != 'Employee-List.csv' or file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Please upload 'Employee-List.csv' as a CSV file.")

    contents = await file.read()
    try:
        employees = process_employee_data(contents)
        assignments = create_secret_santa_assignments(employees)
        final_csv = generate_csv_from_data(assignments)

        file_path = "temp_secret_santa.csv"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_csv)

        return FileResponse(path=file_path, filename="secret_santa_assignments.csv", media_type='text/csv')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Secret Santa Game"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)