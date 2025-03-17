import pytest


@pytest.mark.asyncio
async def test_get_analytics(client):
    response = await client.get("/analytics/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_note_valid(client):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    response = await client.post("/notes/", json=note_data)
    assert response.status_code == 200
    assert response.json()["title"] == note_data["title"]
    assert response.json()["content"] == note_data["content"]


@pytest.mark.asyncio
async def test_create_note_invalid(client):
    note_data = {"title": "", "content": "Content of the note"}
    response = await client.post("/notes/", json=note_data)
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]
    assert (
        response.json()["detail"][0]["msg"] == "String should have at least 1 character"
    )


@pytest.mark.asyncio
async def test_read_notes(client):
    response = await client.get("/notes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_read_note_valid(client):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    create_response = await client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    response = await client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == note_data["title"]


@pytest.mark.asyncio
async def test_read_note_invalid(client):
    response = await client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


@pytest.mark.asyncio
async def test_update_note_valid(client):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    create_response = await client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    updated_data = {"content": "Updated content"}
    response = await client.put(f"/notes/{note_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["content"] == updated_data["content"]
    assert response.json()["title"] == note_data["title"]


@pytest.mark.asyncio
async def test_update_note_invalid(client):
    updated_data = {"title": "Updated Note", "content": "Updated content"}
    response = await client.put("/notes/999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


@pytest.mark.asyncio
async def test_delete_note_valid(client):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    create_response = await client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    response = await client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Note deleted successfully"


@pytest.mark.asyncio
async def test_delete_note_invalid(client):
    response = await client.delete("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


@pytest.mark.asyncio
async def test_summarize_note_valid(client):
    note_data = {
        "title": "Test Note",
        "content": "This is the content of the note that needs to be summarized.",
    }
    create_response = await client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    response = await client.post(f"/notes/{note_id}/summarize")
    assert response.status_code == 200
    assert "summary" in response.json()


@pytest.mark.asyncio
async def test_summarize_note_invalid(client):
    response = await client.post("/notes/999/summarize")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
