from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.utils.field_normalizer import FieldNormalizer
import json

router = APIRouter()

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    data: Dict[str, Any] = Body(..., example={
        "content": "Meeting notes",
        "contact_id": 1
    }),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new note.
    
    The API accepts various field names that will be normalized:
    - For content: "content", "body", "text", "message", "note", "description"
    - For contact_id: "contact_id", "contactId", "contact", "person_id", "personId"
    """
    try:
        # Normalize the data
        normalized_data = FieldNormalizer.normalize_note_data(data)
        
        # Validate required fields
        validation_error = FieldNormalizer.validate_required_fields(normalized_data)
        if validation_error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=validation_error
            )
        
        # Create note using normalized data
        db_note = Note(
            body=normalized_data['content'],
            contact_id=normalized_data['contact_id'],
            author=current_user.username
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[NoteResponse])
async def read_notes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all notes.
    """
    notes = db.query(Note).offset(skip).limit(limit).all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific note by ID.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a note.
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    db_note.body = note.body
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a note.
    """
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    db.delete(db_note)
    db.commit()
    return None 