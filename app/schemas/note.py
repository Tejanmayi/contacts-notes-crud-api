from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    body: str = Field(..., description="The content of the note")
    contact_id: int = Field(..., description="The ID of the contact this note belongs to")

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    body: Optional[str] = None
    contact_id: Optional[int] = None

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) 