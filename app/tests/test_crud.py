import pytest
from app import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


# CREATE
@pytest.mark.asyncio
async def test_create_note(db: AsyncSession):
    note_data = schemas.NoteCreate(title="Test Note", content="Some content")
    note = await crud.create_note(db, note_data)
    assert note.title == "Test Note"
    assert note.content == "Some content"


# READ
@pytest.mark.asyncio
async def test_get_all_notes(db: AsyncSession):
    notes = await crud.get_all_notes(db)
    assert isinstance(notes, list)


@pytest.mark.asyncio
async def test_get_note_by_id(db: AsyncSession):
    note_data = schemas.NoteCreate(title="Test", content="Content")
    new_note = await crud.create_note(db, note_data)
    fetched_note = await crud.get_note_by_id(db, new_note.id)
    assert fetched_note is not None
    assert fetched_note.title == "Test"


@pytest.mark.asyncio
async def test_get_note_by_id_not_found(db: AsyncSession):
    fetched_note = await crud.get_note_by_id(db, 9999)
    assert fetched_note is None


# UPDATE
@pytest.mark.asyncio
async def test_update_note(db: AsyncSession):
    note_data = schemas.NoteCreate(title="Title", content="Old Content")
    note = await crud.create_note(db, note_data)

    updated_data = schemas.NoteUpdate(content="New Content")
    updated_note = await crud.update_note(db, note.id, updated_data)

    assert updated_note.content == "New Content"
    assert updated_note.title == "Title"


@pytest.mark.asyncio
async def test_update_note_partial(db: AsyncSession):
    note_data = schemas.NoteCreate(title="Title", content="Old Content")
    note = await crud.create_note(db, note_data)

    updated_data = schemas.NoteUpdate(content="New Content")
    updated_note = await crud.update_note(db, note.id, updated_data)

    assert updated_note.content == "New Content"
    assert updated_note.title == "Title"

    # Используем select вместо query
    result = await db.execute(
        select(crud.NoteVersion).filter(crud.NoteVersion.note_id == note.id)
    )
    note_version = result.scalar_one_or_none()

    assert note_version is not None
    assert note_version.content == "Old Content"


# DELETE
@pytest.mark.asyncio
async def test_delete_note(db: AsyncSession):
    note_data = schemas.NoteCreate(title="To Delete", content="Content")
    note = await crud.create_note(db, note_data)
    assert await crud.delete_note(db, note.id) is True
    assert await crud.get_note_by_id(db, note.id) is None


@pytest.mark.asyncio
async def test_delete_note_not_found(db: AsyncSession):
    result = await crud.delete_note(db, 9999)
    assert result is False
