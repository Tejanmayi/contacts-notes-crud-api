from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.middleware import RateLimitMiddleware

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

app = FastAPI(
    title="Contact Notes API",
    description="API for managing contacts and their notes",
    version="1.0.0",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "docExpansion": "none",
        "filter": True,
        "syntaxHighlight.theme": "monokai",
        "tryItOutEnabled": True,
        "requestSnippetsEnabled": True,
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "defaultModelRendering": "model",
        "displayOperationId": False,
        "showExtensions": True,
        "showCommonExtensions": True,
        "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"],
        "validatorUrl": None,
        "withCredentials": True,
    }
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
app.middleware("http")(RateLimitMiddleware())

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Contact Notes API"} 