from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import crud, schemas, ai_integration
from typing import List

router = APIRouter()


@router.post("/", response_model=schemas.NoteResponse)
async def create_note(
    note_data: schemas.NoteCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_note(db, note_data)


@router.get("/", response_model=List[schemas.NoteResponse])
async def read_notes(db: AsyncSession = Depends(get_db)):
    notes = await crud.get_all_notes(db)
    return notes


@router.get("/{note_id}", response_model=schemas.NoteResponse)
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=schemas.NoteResponse)
async def update_note(
    note_id: int, note_data: schemas.NoteUpdate, db: AsyncSession = Depends(get_db)
):
    updated_note = await crud.update_note(db, note_id, note_data)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/{note_id}")
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    deleted_note = await crud.delete_note(db, note_id)
    if not deleted_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}


@router.post("/{note_id}/summarize")
async def summarize_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = await ai_integration.summarize_text(note.content)  # Добавляем await
    return {"summary": summary}
