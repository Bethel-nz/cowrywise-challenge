# Library Management System - Cowrywise Challenge

Distributed library app with real-time book management.

## API Routes

### Frontend Service (Port 8181)

```text
Books:
- GET  /books              # List available books
- GET  /books/all          # List all books (including borrowed)
- GET  /books/<id>         # Get specific book
- GET  /books?publisher=X  # Filter by publisher
- GET  /books?category=X   # Filter by category

Users:
- POST /users             # Create new user
  {
    "email": "user@example.com",
    "firstname": "John",
    "lastname": "Doe"
  }

Borrowing:
- POST /books/<id>/borrow # Borrow a book
  {
    "user_id": 1,
    "days": 14
  }
```

### Admin Service (Port 8080)

```text
Books:
- POST   /admin/books           # Add new book
  {
    "title": "Clean Code",
    "publisher": "Prentice Hall",
    "category": "technology"
  }
- DELETE /admin/books/<id>      # Remove book
- GET    /admin/books/unavailable # List borrowed books

Users:
- GET    /admin/users          # List all users
- GET    /admin/users/borrowed # List users with borrowed books

Data Management:
- POST   /admin/drop-data     # Clear admin database
- POST   /drop-data          # Clear frontend database
```

## Design Choice

- **Postgres**: Postgres for write-heavy operations.
- **Redis Pub/Sub**: Lightweight sync for book adds/removals/borrowing—low latency.

## Tech Stack

- Python/Flask: Core APIs.
- PostgreSQL : writes for Transactional operations.
- Redis: Pub/Sub for sync.
- Docker: Containerized deployment.

## Quick Start

```bash
docker compose up          # ADMIN: 8080, Frontend: 8181
docker compose -f docker-compose.test.yml up  # Run tests
```

**Note**: I would like to state that i have 0 experience using python, the tests are not up to standard and i would like to apologize for that as they would fail.
