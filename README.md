# Library Management System

Example FastAPI application for the **Devscale Indonesia AI-Enabled Python Webdev Program Batch III**.

This is a complete library management system demonstrating production-ready REST API development with Python, FastAPI, and SQLModel.

## Features

- **Books Management**: CRUD operations for books with ISBN validation
- **Members Management**: Member registration and management
- **Borrowing System**: Track book loans with return functionality
- **Availability Tracking**: Real-time book availability status
- **API Documentation**: Interactive API docs via Scalar

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLModel** - SQL databases in Python, designed for simplicity
- **SQLite** - Lightweight database (production: PostgreSQL)
- **Pydantic** - Data validation using Python type hints
- **UV** - Fast Python package installer and resolver

## Quick Start

### Prerequisites

- Python 3.11+
- UV installed

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd fastapi-apps

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### Run the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, access the interactive API documentation:

- **Scalar UI**: `http://localhost:8000/scalar`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## API Endpoints

### Books
- `GET /books` - List all books
- `GET /books/{id}` - Get book by ID
- `POST /books` - Create new book
- `PUT /books/{id}` - Update book
- `DELETE /books/{id}` - Delete book

### Members
- `GET /members` - List all members
- `GET /members/{id}` - Get member by ID
- `POST /members` - Create new member
- `PUT /members/{id}` - Update member
- `DELETE /members/{id}` - Delete member

### Borrowing Records
- `GET /borrowings` - List all borrowing records
- `GET /borrowings/{borrow_id}` - Get record by ID
- `POST /borrowings` - Create borrowing record
- `PUT /borrowings/{borrow_id}` - Update record
- `DELETE /borrowings/{borrow_id}` - Delete record
- `POST /borrowings/{borrow_id}/return` - Return borrowed book

## Project Structure

```
app/
├── main.py                 # Application entry point
├── router/                 # API route handlers
│   ├── books.py           # Books endpoints
│   ├── members.py         # Members endpoints
│   └── borrowing_history.py # Borrowing records endpoints
├── models/                # Database models
│   ├── models.py          # SQLModel table definitions
│   └── engine.py          # Database engine & session
└── schema/                # Pydantic schemas
    └── schemas.py         # Request/response models
```

## Example Usage

### Create a Book
```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Python Programming",
    "author": "Guido van Rossum",
    "isbn": "978-0-13-110362-7"
  }'
```

### Create a Member
```bash
curl -X POST "http://localhost:8000/members" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'
```

### Borrow a Book
```bash
curl -X POST "http://localhost:8000/borrowings" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1,
    "borrow_date": "2024-01-15"
  }'
```

### Return a Book
```bash
curl -X POST "http://localhost:8000/borrowings/1/return"
```

## CORS Configuration

This application is configured to accept requests from any origin (CORS enabled for `*`), making it suitable for frontend development on any domain.

## Database

By default, the application uses SQLite. The database file is created automatically on first run.

For production, configure a PostgreSQL connection string in your environment:

```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Optional: Custom database URL
DATABASE_URL=sqlite:///library.db

# Optional: Application settings
DEBUG=true
```

## Learning Objectives

This example demonstrates:

- ✅ FastAPI route handlers with dependency injection
- ✅ SQLModel ORM with relationships
- ✅ Pydantic data validation and serialization
- ✅ CRUD operations with proper HTTP semantics
- ✅ Error handling with HTTP exceptions
- ✅ CORS configuration for frontend integration
- ✅ Project structure and organization
- ✅ API documentation generation

## License

MIT License - Created for educational purposes.

---

**Devscale Indonesia** - AI-Enabled Python Webdev Program Batch III
