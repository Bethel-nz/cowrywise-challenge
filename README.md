# Library Management System - Cowrywise Challenge

A distributed library app with admin and frontend services, built for real-time book management.

## Features

- **Frontend**: View all books, borrow books, check unavailable books.
- **Admin**: Borrowing logic + book management.
- **Real-Time**: Redis Pub/Sub syncs borrowing events across services.

## Tech Stack

- **Python/Flask**: Backend + Admin APIs.
- **PostgreSQL**: Separate DBs for admin and frontend.
- **Redis**: Pub/Sub for interservice communication.
- **Docker**: Containerized for easy spins.

## Quick Start

```bash
 docker compose up          # Start services (ADMIN: 8080, Frontend: 8181)
 docker compose -f docker-compose.test.yml up  # Run tests
```

## Notes

- The `docker-compose.test.yml` file is used to run the tests.
- The `docker-compose.yml` file is used to start the services.
