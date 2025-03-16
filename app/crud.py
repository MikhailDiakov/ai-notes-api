from sqlalchemy.orm import Session
from .schemas import NoteCreate, NoteUpdate
from .models import Note, NoteVersion


def create_note(db: Session, note_data: NoteCreate):
    note = Note(title=note_data.title, content=note_data.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_note_by_id(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()


def update_note(db: Session, note_id: int, note_data: NoteUpdate):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note_version = NoteVersion(note_id=note.id, content=note.content)
        db.add(note_version)
        note.content = note_data.content
        db.commit()
        db.refresh(note)
    return note


def delete_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note


def get_all_notes(db: Session):
    return db.query(Note).all()
