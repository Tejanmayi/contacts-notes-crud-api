from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class NoteBase(BaseModel):
    """Base schema for note data."""
    body: str = Field(..., description="Content of the note")
    contact_id: int = Field(..., description="ID of the associated contact")

class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass

class NoteUpdate(BaseModel):
    """Schema for updating an existing note."""
    body: str = Field(..., description="Content of the note")

class NoteInDB(NoteBase):
    """Schema for note data in the database."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NoteResponse(NoteInDB):
    """Schema for note response."""
    pass 