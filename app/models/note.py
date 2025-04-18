from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    author = Column(Text, nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Use string reference for relationship to avoid circular imports
    contact = relationship("Contact", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.id}>"

    def to_dict(self):
        """Convert the note to a dictionary."""
        return {
            "id": self.id,
            "body": self.body,
            "author": self.author,
            "contact_id": self.contact_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 