from fastapi import APIRouter
from app.api.v1.endpoints import contacts, notes, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"]) 