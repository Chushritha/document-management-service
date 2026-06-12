# 📄 Document Management Service

A simple FastAPI backend to upload, list, and delete documents.

---

## 🛠️ Setup Instructions

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd document_service
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

Server will start at: **http://127.0.0.1:8000**

---

## 📬 API Usage Examples

### ✅ Upload a Document
```bash
curl -X POST http://127.0.0.1:8000/documents \
  -F "file=@resume.pdf"
```

**Response:**
```json
{
  "id": 1,
  "filename": "resume.pdf",
  "size": 125634,
  "uploaded_at": "2026-06-11T10:00:00Z"
}
```

---

### 📋 List All Documents
```bash
curl http://127.0.0.1:8000/documents
```

---

### ❌ Delete a Document
```bash
curl -X DELETE http://127.0.0.1:8000/documents/1
```

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

---

## 📌 Notes
- Supported file types: `.pdf`, `.docx`, `.txt`
- Max file size: **10 MB**
- Files are stored in the `uploaded_files/` folder
- Database: SQLite (`documents.db` auto-created)
- Interactive API docs available at: **http://127.0.0.1:8000/docs**
