from app import crud, schemas
import pytest


# POST
def test_create_note(db):
    note_data = schemas.NoteCreate(title="Test Note", content="Some content")
    note = crud.create_note(db, note_data)
    assert note.title == "Test Note"
    assert note.content == "Some content"


# GET
def test_get_all_notes(db):
    notes = crud.get_all_notes(db)
    assert isinstance(notes, list)


def test_get_note_by_id(db):
    note_data = schemas.NoteCreate(title="Test", content="Content")
    new_note = crud.create_note(db, note_data)
    fetched_note = crud.get_note_by_id(db, new_note.id)
    assert fetched_note is not None
    assert fetched_note.title == "Test"


def test_get_note_by_id_not_found(db):
    fetched_note = crud.get_note_by_id(db, 9999)
    assert fetched_note is None


# UPDATE
def test_update_note(db):
    note_data = schemas.NoteCreate(title="Title", content="Old Content")
    note = crud.create_note(db, note_data)

    updated_data = schemas.NoteUpdate(content="New Content")
    updated_note = crud.update_note(db, note.id, updated_data)

    assert updated_note.content == "New Content"
    assert updated_note.title == "Title"


def test_update_note_partial(db):
    note_data = schemas.NoteCreate(title="Title", content="Old Content")
    note = crud.create_note(db, note_data)

    updated_data = schemas.NoteUpdate(content="New Content")
    updated_note = crud.update_note(db, note.id, updated_data)

    assert updated_note.content == "New Content"
    assert updated_note.title == "Title"

    note_version = (
        db.query(crud.NoteVersion).filter(crud.NoteVersion.note_id == note.id).first()
    )
    assert note_version is not None
    assert note_version.content == "Old Content"


# DELETE
def test_delete_note(db):
    note_data = schemas.NoteCreate(title="To Delete", content="Content")
    note = crud.create_note(db, note_data)
    assert crud.delete_note(db, note.id) is True
    assert crud.get_note_by_id(db, note.id) is None


def test_delete_note_not_found(db):
    result = crud.delete_note(db, 9999)
    assert result is False
