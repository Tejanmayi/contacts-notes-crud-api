from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Note(BaseModel):
    __tablename__ = "notes"

    body = Column(Text, nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    contact = relationship("Contact", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.id} for Contact {self.contact_id}>" 