from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)       # Auto ID
    filename = Column(String, nullable=False)                 # Original file name
    file_path = Column(String, nullable=False)               # Where file is saved
    size = Column(Integer, nullable=False)                   # File size in bytes
    uploaded_at = Column(DateTime(timezone=True), nullable=False)  # Upload time
