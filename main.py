import os
import shutil
from datetime import datetime, timezone

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
from models import Document
from schemas import DocumentResponse, DeleteResponse

# Create all tables in DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Document Management Service")

# Folder to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file types and max size
ALLOWED_TYPES = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"}
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes


# ✅ Upload Document
@app.post("/documents", response_model=DocumentResponse, status_code=201)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # 1. Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: PDF, DOCX, TXT")

    # 2. Read file content and check size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB limit")

    # 3. Save file to local filesystem
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            f.write(file_content)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save file")

    # 4. Save metadata to database
    doc = Document(
        filename=file.filename,
        file_path=file_path,
        size=len(file_content),
        uploaded_at=datetime.now(timezone.utc)
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc


# ✅ List All Documents
@app.get("/documents", response_model=List[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents


# ✅ Delete Document
@app.delete("/documents/{document_id}", response_model=DeleteResponse)
def delete_document(document_id: int, db: Session = Depends(get_db)):

    # 1. Find document in DB
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2. Delete file from filesystem
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to delete file")

    # 3. Delete from database
    db.delete(doc)
    db.commit()

    return {"message": "Document deleted successfully"}
