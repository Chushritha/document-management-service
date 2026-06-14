# Document Management Service

## My Approach

When I started this project, my goal was to keep the code clean, simple, and easy to understand.

I broke the problem into three clear API endpoints - Upload, List, and Delete.

### How I Structured the Code

Instead of writing everything in one file, I separated code into focused modules:
- database.py handles SQLite connection setup
- models.py defines the documents table structure
- schemas.py controls API response shape and hides file_path for security
- main.py contains all 3 APIs with validation and error handling
- requirements.txt lists all packages needed to run the project

### File Upload Flow
1. Validate file extension - only PDF DOCX TXT allowed
2. Check file size - maximum 10 MB
3. Save file to uploaded_files folder
4. Save metadata to SQLite database
5. Return response with id filename size uploaded_at

### Error Handling
- 400 for unsupported file type or size exceeded
- 404 for document not found
- 500 for unexpected server error

### Why This Structure
I followed Separation of Concerns - each file has one clear responsibility.
This makes code easier to read test and maintain.

## Tech Stack
Python 3.10+ FastAPI SQLite SQLAlchemy Pydantic Uvicorn

## Setup
pip install -r requirements.txt
uvicorn main:app --reload
Open http://127.0.0.1:8000/docs
