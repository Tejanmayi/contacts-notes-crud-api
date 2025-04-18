# Contact Notes API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints, include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Authentication Endpoints

#### Login
```http
POST /auth/login
```

Authenticate a user and receive a JWT token.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

**Status Codes:**
- `200 OK`: Successfully authenticated
- `401 Unauthorized`: Invalid credentials

#### Register
```http
POST /auth/register
```

Register a new user.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "is_active": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Status Codes:**
- `201 Created`: User successfully created
- `400 Bad Request`: Invalid input or user already exists

## Contacts

### Create Contact
```http
POST /contacts/
```

Create a new contact.

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "phone": "string",
  "company": "string",
  "title": "string"
}
```

**Response:**
```json
{
    "id": "integer",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string",
    "company": "string",
    "title": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Status Codes:**
- `201 Created`: Contact successfully created
- `422 Unprocessable Entity`: Invalid input data

### Get All Contacts
```http
GET /contacts/
```

Retrieve all contacts with pagination.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
    {
        "id": "integer",
        "first_name": "string",
        "last_name": "string",
        "email": "string",
        "phone": "string",
        "company": "string",
        "title": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
]
```

### Get Contact by ID
```http
GET /contacts/{contact_id}
```

Retrieve a specific contact by ID.

**Response:**
```json
{
    "id": "integer",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string",
    "company": "string",
    "title": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Status Codes:**
- `200 OK`: Contact found
- `404 Not Found`: Contact not found

### Update Contact
```http
PUT /contacts/{contact_id}
```

Update an existing contact.

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "phone": "string",
  "company": "string",
  "title": "string"
}
```

**Response:**
```json
{
    "id": "integer",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone": "string",
    "company": "string",
    "title": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Status Codes:**
- `200 OK`: Contact updated
- `404 Not Found`: Contact not found
- `422 Unprocessable Entity`: Invalid input data

### Delete Contact
```http
DELETE /contacts/{contact_id}
```

Delete a contact.

**Status Codes:**
- `204 No Content`: Contact successfully deleted
- `404 Not Found`: Contact not found

## Notes

### Create Note
```http
POST /notes/
```

Create a new note for a contact.

**Request Body:**
The API accepts various field names that will be normalized. Here are the accepted variations:

For the note content:
```json
{
    "content": "string",  // or "body", "text", "message", "note", "description"
    "contact_id": "integer"  // or "contactId", "contact", "person_id", "personId"
}
```

**Response:**
```json
{
    "id": "integer",
    "body": "string",
    "author": "string",
    "contact_id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Status Codes:**
- `201 Created`: Note successfully created
- `422 Unprocessable Entity`: Invalid input data
- `404 Not Found`: Contact not found

### Get All Notes
```http
GET /notes/
```

Retrieve all notes with pagination.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records to return (default: 100)

**Response:**
```json
[
    {
        "id": "integer",
        "body": "string",
        "author": "string",
        "contact_id": "integer",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
]
```

### Get Note by ID
```http
GET /notes/{note_id}
```

Retrieve a specific note by ID.

**Response:**
```json
{
    "id": "integer",
    "body": "string",
    "author": "string",
    "contact_id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Status Codes:**
- `200 OK`: Note found
- `404 Not Found`: Note not found

### Update Note
```http
PUT /notes/{note_id}
```

Update an existing note.

**Request Body:**
```json
{
    "body": "string"
}
```

**Response:**
```json
{
    "id": "integer",
    "body": "string",
    "author": "string",
    "contact_id": "integer",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

**Status Codes:**
- `200 OK`: Note updated
- `404 Not Found`: Note not found
- `422 Unprocessable Entity`: Invalid input data

### Delete Note
```http
DELETE /notes/{note_id}
```

Delete a note.

**Status Codes:**
- `204 No Content`: Note successfully deleted
- `404 Not Found`: Note not found

## Error Responses

The API uses conventional HTTP response codes to indicate the success or failure of an API request.

- `200 OK`: Successfully retrieved data
- `201 Created`: Successfully created resource
- `204 No Content`: Successfully deleted resource
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Authentication failed or token missing
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses will include a message:

```json
{
    "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Current limits are:
- 100 requests per minute per IP address
- 1000 requests per hour per IP address

When rate limit is exceeded, the API will return:
- Status Code: `429 Too Many Requests`
- Headers will include `X-RateLimit-Limit` and `X-RateLimit-Remaining` 