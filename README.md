# Contact Notes System

A robust backend service for managing contact notes with authentication, rate limiting, and event-driven processing.

## Features

- JWT-based authentication
- CRUD operations for Contacts and Notes
- Rate limiting with exponential backoff
- Event-driven note processing using Celery
- Field normalization for note data
- Comprehensive error handling
- Interactive API documentation (Swagger UI)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Mac: source venv/bin/activate 
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
.env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Start the Redis server (required for Celery):
```bash
# On Windows, download and run Redis server
# On Linux/Mac: redis-server
```

6. Start the Celery worker:
```bash
celery -A app.worker worker --loglevel=info
```

7. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Documentation

The API documentation is available at http://localhost:8000/docs. The Swagger UI provides an interactive interface to test all endpoints.

### Using the Swagger UI

1. **Access the Documentation**:
   - Open http://localhost:8000/docs in your browser
   - You'll see all available endpoints organized by tags (auth, contacts, notes)

2. **Authentication**:
   - Click the "Authorize" button at the top of the page
   - You have two options:
     a. **Login with credentials**:
        - Enter your username and password
        - Click "Authorize"
        - The token will be automatically obtained and stored
     b. **Use existing token**:
        - Enter your token in the format: `Bearer your_token_here`
        - Click "Authorize"

3. **Making Authenticated Requests**:
   - After authorization, all requests will automatically include the token
   - The token persists between page refreshes
   - You can test all endpoints directly from the UI

### Authentication Flow

1. **Register a new user**:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}'
```

2. **Get an access token**:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=your_username&password=your_password'
```

3. **Use the access token**:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/contacts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "company": "Example Corp",
  "title": "Developer"
}'
```

## Key Decisions and Tradeoffs

1. **Authentication**: JWT-based auth for stateless authentication and easy scaling
2. **Database**: SQLAlchemy for ORM with PostgreSQL for reliable data storage
3. **Async Processing**: Celery for background tasks and event-driven architecture
4. **Rate Limiting**: Redis-based rate limiting with exponential backoff
5. **Error Handling**: Comprehensive error handling with custom exceptions
6. **Documentation**: Interactive Swagger UI with persistent authentication

## Future Improvements

1. Add caching layer for frequently accessed contacts
2. Implement WebSocket for real-time updates
3. Add audit logging for all operations
4. Implement role-based access control
5. Add bulk operations for contacts and notes
6. Implement search functionality with Elasticsearch
7. Add data export/import capabilities 