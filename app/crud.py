from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .schemas import NoteCreate, NoteUpdate
from .models import Note, NoteVersion


async def create_note(db: AsyncSession, note_data: NoteCreate):
    note = Note(title=note_data.title, content=note_data.content)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_all_notes(db: AsyncSession):
    result = await db.execute(select(Note))
    return result.scalars().all()


async def get_note_by_id(db: AsyncSession, note_id: int):
    result = await db.execute(select(Note).filter(Note.id == note_id))
    return result.scalars().first()


async def update_note(db: AsyncSession, note_id: int, note_data: NoteUpdate):
    result = await db.execute(select(Note).filter(Note.id == note_id))
    note = result.scalars().first()
    if note:
        note_version = NoteVersion(note_id=note.id, content=note.content)
        db.add(note_version)
        note.content = note_data.content
        await db.commit()
        await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note_id: int):
    result = await db.execute(select(Note).filter(Note.id == note_id))
    note = result.scalars().first()
    if note:
        await db.delete(note)
        await db.commit()
        return True
    return False
