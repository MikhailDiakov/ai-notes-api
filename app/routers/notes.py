from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas, ai_integration
from typing import List

router = APIRouter()


@router.post("/", response_model=schemas.NoteResponse)
def create_note(note_data: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, note_data)


@router.get("/", response_model=List[schemas.NoteResponse])
def read_notes(db: Session = Depends(get_db)):
    notes = crud.get_all_notes(db)
    return notes


@router.get("/{note_id}", response_model=schemas.NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id: int, note_data: schemas.NoteUpdate, db: Session = Depends(get_db)
):
    updated_note = crud.update_note(db, note_id, note_data)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    deleted_note = crud.delete_note(db, note_id)
    if not deleted_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}


@router.post("/{note_id}/summarize")
def summarize_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = ai_integration.summarize_text(note.content)
    return {"summary": summary}
