from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    versions = relationship(
        "NoteVersion", back_populates="note", cascade="all, delete-orphan"
    )


class NoteVersion(Base):
    __tablename__ = "note_versions"
    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(
        Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    note = relationship("Note", back_populates="versions")
