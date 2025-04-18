from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Contact(BaseModel):
    __tablename__ = "contacts"

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    company = Column(String(100))
    title = Column(String(100))
    notes = relationship("Note", back_populates="contact", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name}>" 