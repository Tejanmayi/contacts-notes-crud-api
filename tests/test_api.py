from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.contact import Contact
from app.models.note import Note
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_contact(db):
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "company": "Test Corp",
        "title": "Developer"
    }
    response = client.post("/api/v1/contacts/", json=contact_data)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == contact_data["first_name"]
    assert data["email"] == contact_data["email"]

def test_get_contacts(db):
    response = client.get("/api/v1/contacts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_create_note(db):
    # First, create a contact
    contact_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com"
    }
    contact_response = client.post("/api/v1/contacts/", json=contact_data)
    contact_id = contact_response.json()["id"]

    # Then create a note for that contact
    note_data = {
        "body": "Test note content",
        "contact_id": contact_id
    }
    response = client.post("/api/v1/notes/", json=note_data)
    assert response.status_code == 201
    data = response.json()
    assert data["body"] == note_data["body"]
    assert data["contact_id"] == contact_id

def test_get_notes(db):
    response = client.get("/api/v1/notes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_contact(db):
    # Create a contact first
    contact_data = {
        "first_name": "Update",
        "last_name": "Test",
        "email": "update.test@example.com"
    }
    create_response = client.post("/api/v1/contacts/", json=contact_data)
    contact_id = create_response.json()["id"]

    # Update the contact
    update_data = {
        "first_name": "Updated",
        "company": "New Company"
    }
    response = client.put(f"/api/v1/contacts/{contact_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["company"] == update_data["company"]

def test_delete_contact(db):
    # Create a contact first
    contact_data = {
        "first_name": "Delete",
        "last_name": "Test",
        "email": "delete.test@example.com"
    }
    create_response = client.post("/api/v1/contacts/", json=contact_data)
    contact_id = create_response.json()["id"]

    # Delete the contact
    response = client.delete(f"/api/v1/contacts/{contact_id}")
    assert response.status_code == 204

    # Verify the contact is deleted
    get_response = client.get(f"/api/v1/contacts/{contact_id}")
    assert get_response.status_code == 404 