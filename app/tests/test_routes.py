def test_get_analytics(client, db):
    response = client.get("/analytics/")
    assert response.status_code == 200


def test_create_note_valid(client, db):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    response = client.post("/notes/", json=note_data)
    assert response.status_code == 200
    assert response.json()["title"] == note_data["title"]
    assert response.json()["content"] == note_data["content"]


def test_create_note_invalid(client, db):
    note_data = {"title": "", "content": "Content of the note"}
    response = client.post("/notes/", json=note_data)
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]
    assert (
        response.json()["detail"][0]["msg"] == "String should have at least 1 character"
    )


def test_read_notes(client, db):
    response = client.get("/notes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_note_valid(client, db):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    create_response = client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["title"] == note_data["title"]


def test_read_note_invalid(client, db):
    response = client.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_update_note_valid(client, db):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    create_response = client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    updated_data = {"content": "Updated content"}
    response = client.put(f"/notes/{note_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["content"] == updated_data["content"]
    assert response.json()["title"] == note_data["title"]


def test_update_note_invalid(client, db):
    updated_data = {"title": "Updated Note", "content": "Updated content"}
    response = client.put("/notes/999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_delete_note_valid(client, db):
    note_data = {"title": "Test Note", "content": "Content of the note"}
    create_response = client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Note deleted successfully"


def test_delete_note_invalid(client, db):
    response = client.delete("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"


def test_summarize_note_valid(client, db):
    note_data = {
        "title": "Test Note",
        "content": "This is the content of the note that needs to be summarized.",
    }
    create_response = client.post("/notes/", json=note_data)
    note_id = create_response.json()["id"]

    response = client.post(f"/notes/{note_id}/summarize")
    assert response.status_code == 200
    assert "summary" in response.json()


def test_summarize_note_invalid(client, db):
    response = client.post("/notes/999/summarize")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
