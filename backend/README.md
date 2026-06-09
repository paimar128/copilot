# Backend JWT API

A FastAPI web application that implements JWT (JSON Web Token) authentication with login and token refresh endpoints.

## Features

- **POST `/auth/login`** – Authenticate with username and password; returns a JWT access token (300 s expiry) and a refresh token (7 days expiry).
- **POST `/auth/refresh`** – Exchange a valid refresh token for a new pair of tokens.
- **GET `/health`** – Health-check endpoint.
- Interactive API docs at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## Credentials

| Username | Password  |
|----------|-----------|
| `admin`  | `admin123`|

## Tech Stack

| Tool           | Purpose                      |
|----------------|------------------------------|
| Python 3.11    | Runtime                      |
| FastAPI 0.115  | Web framework                |
| PyJWT 2.12     | JWT encoding / decoding      |
| bcrypt 4.x     | Password hashing             |
| Uvicorn        | ASGI server                  |
| Poetry         | Dependency management        |
| Docker         | Containerisation             |

---

## Getting Started

### Prerequisites

- [Python 3.11+](https://www.python.org/)
- [Poetry](https://python-poetry.org/docs/#installation)

### Local development

```bash
# 1. Install dependencies
cd backend
poetry install

# 2. Run the server
poetry run uvicorn app.main:app --reload

# 3. Open the interactive docs
open http://localhost:8000/docs
```

### Environment variables

| Variable     | Default                                   | Description                         |
|--------------|-------------------------------------------|-------------------------------------|
| `SECRET_KEY` | `changeme-super-secret-key-for-dev-only`  | HMAC secret used to sign JWT tokens |

> **Important:** Always set a strong, random `SECRET_KEY` in production.

---

## Docker

### Build and run with Docker Compose

```bash
cd backend

# (Optional) set a custom secret key
export SECRET_KEY="your-strong-random-secret"

docker compose up --build
```

The API will be available at `http://localhost:8000`.

### Build the image manually

```bash
docker build -t backend-jwt .
docker run -p 8000:8000 -e SECRET_KEY="your-strong-random-secret" backend-jwt
```

---

## API Usage

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**

```json
{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### Refresh token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<your-refresh-token>"}'
```

**Response:** same structure as `/auth/login`.

### Health check

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

---

## Running Tests

```bash
cd backend
poetry run pytest -v
```

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   └── auth/
│       ├── __init__.py
│       ├── router.py      # /auth endpoints
│       ├── schemas.py     # Pydantic request/response models
│       └── security.py    # JWT helpers & password hashing
├── tests/
│   └── test_auth.py       # Endpoint tests
├── pyproject.toml         # Poetry project & dependencies
├── Dockerfile
├── docker-compose.yml
└── README.md
```
